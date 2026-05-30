import { run, claudeCode } from "@ai-hero/sandcastle";
import { docker } from "@ai-hero/sandcastle/sandboxes/docker";
import { execFileSync } from "node:child_process";
import { fileURLToPath } from "node:url";

// Host orchestrator for Scrython. Works open issues labeled `ready-for-agent`,
// one sandboxed agent per issue, fanned out in parallel. Each agent commits
// only; the host pushes, opens a PR, and relabels the issue to `needs-review`.
//
// Unlike a plain fan-out, this respects the `## Blocked by` section in an issue
// body: an issue is only dispatched once every blocker it names is cleared.
// Scrython's connector series (#170 -> #171 -> #172/#173) relies on this so a
// later slice never branches off a base that lacks the earlier slice's work.

const REPO = "NandaScott/Scrython";
const AGENT_LABEL = "ready-for-agent";
const DONE_LABEL = "needs-review";
const IMAGE_NAME = "sandcastle:scrython";
const MODEL = "claude-sonnet-4-6";
const DEFAULT_BASE = "develop";
const DRY_RUN = process.env.DRY_RUN === "1";

const promptFile = fileURLToPath(new URL("./prompt.md", import.meta.url));

interface Issue {
  readonly number: number;
  readonly title: string;
  readonly body: string;
}

interface Plan {
  readonly issue: Issue;
  readonly target: string;
}

interface Outcome {
  readonly number: number;
  readonly target: string;
  readonly status: string;
  readonly detail: string;
}

function git(...args: string[]): string {
  return execFileSync("git", args, { encoding: "utf8" }).trim();
}

function gh(...args: string[]): string {
  return execFileSync("gh", args, { encoding: "utf8" }).trim();
}

function errorMessage(value: unknown): string {
  return value instanceof Error ? value.message : String(value);
}

// Parse the ONLY_ISSUE selector into a set of issue numbers. Accepts a single
// number (`170`), a comma-separated list (`170,172,173`), an inclusive range
// (`170-173`), or any mix (`170-172,180`). Returns null when unset, so the run
// falls back to every ready-for-agent issue.
function parseIssueSelection(raw: string | undefined): Set<number> | null {
  if (!raw) {
    return null;
  }
  const selected = new Set<number>();
  for (const term of raw.split(",")) {
    const trimmed = term.trim();
    if (trimmed === "") {
      continue;
    }
    const range = trimmed.match(/^(\d+)\s*-\s*(\d+)$/);
    if (range) {
      const start = Number(range[1]);
      const end = Number(range[2]);
      if (start > end) {
        throw new Error(`ONLY_ISSUE range "${trimmed}" is descending; use low-high.`);
      }
      for (let issueNumber = start; issueNumber <= end; issueNumber++) {
        selected.add(issueNumber);
      }
      continue;
    }
    if (!/^\d+$/.test(trimmed)) {
      throw new Error(`ONLY_ISSUE term "${trimmed}" is not a number or range.`);
    }
    selected.add(Number(trimmed));
  }
  if (selected.size === 0) {
    throw new Error(`ONLY_ISSUE="${raw}" selected no issues.`);
  }
  return selected;
}

const ONLY_ISSUES = parseIssueSelection(process.env.ONLY_ISSUE);

function slugify(title: string): string {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-+|-+$/g, "");
}

// The integration branch comes from the slice's parent PRD, not a milestone:
// a milestone groups several PRDs, so it is the wrong granularity for a branch.
// The parent PRD reference lives in the issue's `## Parent` section.
function parseParent(body: string): number | null {
  const section = body.match(/##\s*Parent\s*([\s\S]*?)(?:\n#{1,6}\s|$)/i);
  if (!section) {
    return null;
  }
  const match = section[1].match(/#(\d+)/);
  return match ? Number(match[1]) : null;
}

// Turn a PRD issue title into a branch slug, dropping a leading `PRD:` and any
// trailing parenthetical, so `PRD: ScryfallConnector refactor (PR 1 of a series)`
// becomes `scryfallconnector-refactor`.
function prdSlug(prdTitle: string): string {
  const core = prdTitle.replace(/^\s*PRD:\s*/i, "").split("(")[0];
  return slugify(core);
}

const issueTitleCache = new Map<number, string>();

function issueTitle(issueNumber: number): string {
  const cached = issueTitleCache.get(issueNumber);
  if (cached) {
    return cached;
  }
  const title = JSON.parse(
    gh("issue", "view", String(issueNumber), "--repo", REPO, "--json", "title"),
  ).title as string;
  issueTitleCache.set(issueNumber, title);
  return title;
}

function targetBranchFor(issue: Issue): string {
  const parent = parseParent(issue.body);
  if (parent === null) {
    return DEFAULT_BASE;
  }
  return `prd/${prdSlug(issueTitle(parent))}`;
}

// Pull the issue numbers out of the `## Blocked by` section only, so a `## Parent`
// reference (or any other `#N` in the body) is never mistaken for a blocker.
function parseBlockers(body: string): number[] {
  const section = body.match(/##\s*Blocked by\s*([\s\S]*?)(?:\n#{1,6}\s|$)/i);
  if (!section) {
    return [];
  }
  const numbers = [...section[1].matchAll(/#(\d+)/g)].map((match) => Number(match[1]));
  return [...new Set(numbers)];
}

const issueStateCache = new Map<number, string>();

function issueState(issueNumber: number): string {
  const cached = issueStateCache.get(issueNumber);
  if (cached) {
    return cached;
  }
  const state = JSON.parse(
    gh("issue", "view", String(issueNumber), "--repo", REPO, "--json", "state"),
  ).state as string;
  issueStateCache.set(issueNumber, state);
  return state;
}

// A blocker is cleared when its issue is closed, or when the target base branch
// already contains a commit that references it (e.g. `... (#170)`). The commit
// check is what makes PRD-branch flows work: merging a slice's PR into a
// `prd/<slug>` branch does not close the issue (auto-close only fires on the
// default branch), but it does land a `(#N)` commit on the target.
function blockerCleared(blocker: number, target: string): boolean {
  if (issueState(blocker) === "CLOSED") {
    return true;
  }
  try {
    const log = execFileSync(
      "git",
      ["log", `origin/${target}`, `--grep=(#${blocker})`, "--oneline"],
      { encoding: "utf8", stdio: ["ignore", "pipe", "ignore"] },
    );
    return log.trim().length > 0;
  } catch {
    return false;
  }
}

function pendingBlockers(issue: Issue, target: string): number[] {
  return parseBlockers(issue.body).filter((blocker) => !blockerCleared(blocker, target));
}

function remoteBranchExists(branch: string): boolean {
  const out = execFileSync("git", ["ls-remote", "--heads", "origin", branch], {
    encoding: "utf8",
  });
  return out.trim().length > 0;
}

function ensurePrdBranch(branch: string): void {
  if (remoteBranchExists(branch)) {
    console.log(`PRD branch exists: ${branch}`);
    return;
  }
  if (DRY_RUN) {
    console.log(`[dry-run] would create PRD branch ${branch} from origin/${DEFAULT_BASE}`);
    return;
  }
  console.log(`Creating PRD branch ${branch} from origin/${DEFAULT_BASE}`);
  git("push", "origin", `origin/${DEFAULT_BASE}:refs/heads/${branch}`);
  git("fetch", "origin", `${branch}:${branch}`);
}

async function runIssue(plan: Plan) {
  const branch = `sandcastle/issue-${plan.issue.number}`;
  const result = await run({
    agent: claudeCode(MODEL),
    sandbox: docker({ imageName: IMAGE_NAME }),
    branchStrategy: { type: "branch", branch, baseBranch: plan.target },
    promptFile,
    promptArgs: {
      ISSUE_NUMBER: String(plan.issue.number),
      ISSUE_TITLE: plan.issue.title,
      ISSUE_BODY: plan.issue.body ?? "",
      BASE_BRANCH: plan.target,
    },
    name: `issue-${plan.issue.number}`,
  });
  return { plan, branch, result };
}

function openPullRequest(plan: Plan, branch: string, commitCount: number): Outcome {
  try {
    git("push", "origin", branch);
    const prUrl = gh(
      "pr",
      "create",
      "--repo",
      REPO,
      "--base",
      plan.target,
      "--head",
      branch,
      "--title",
      plan.issue.title,
      "--body",
      `Closes #${plan.issue.number}\n\nOpened by Sandcastle. ${commitCount} commit(s) on \`${branch}\`.`,
    );
    gh(
      "issue",
      "edit",
      String(plan.issue.number),
      "--repo",
      REPO,
      "--remove-label",
      AGENT_LABEL,
      "--add-label",
      DONE_LABEL,
    );
    return { number: plan.issue.number, target: plan.target, status: "PR opened", detail: prUrl };
  } catch (err) {
    return {
      number: plan.issue.number,
      target: plan.target,
      status: "post-run failed",
      detail: errorMessage(err),
    };
  }
}

function printSummary(outcomes: readonly Outcome[]): void {
  console.log("\n=== Sandcastle run summary ===");
  for (const outcome of outcomes) {
    console.log(`#${outcome.number}  ${outcome.target}  ${outcome.status}  ${outcome.detail}`);
  }
}

const allIssues: Issue[] = JSON.parse(
  gh(
    "issue",
    "list",
    "--repo",
    REPO,
    "--label",
    AGENT_LABEL,
    "--state",
    "open",
    "--json",
    "number,title,body",
  ),
);

const issues = ONLY_ISSUES
  ? allIssues.filter((issue) => ONLY_ISSUES.has(issue.number))
  : allIssues;

if (ONLY_ISSUES && issues.length === 0) {
  const requested = [...ONLY_ISSUES].map((n) => `#${n}`).join(", ");
  console.log(`None of ${requested} are open with label ${AGENT_LABEL}. Nothing to do.`);
  process.exit(1);
}

if (issues.length === 0) {
  console.log(`No open issues labeled ${AGENT_LABEL}. Nothing to do.`);
  process.exit(0);
}

if (ONLY_ISSUES) {
  const requested = [...ONLY_ISSUES].map((n) => `#${n}`).join(", ");
  console.log(`ONLY_ISSUE — restricting this run to ${requested}.`);
}

git("fetch", "origin");

// Ensure every PRD branch exists before resolving blockers, since a blocker can
// be cleared by a `(#N)` commit already merged onto that branch.
const targets = new Map(issues.map((issue) => [issue.number, targetBranchFor(issue)]));
const prdBranches = [...new Set(targets.values())].filter((b) => b !== DEFAULT_BASE);
for (const branch of prdBranches) {
  ensurePrdBranch(branch);
}
if (prdBranches.length > 0 && !DRY_RUN) {
  git("fetch", "origin");
}

const plans: Plan[] = [];
const skipped: Outcome[] = [];
for (const issue of issues) {
  const target = targets.get(issue.number)!;
  const pending = pendingBlockers(issue, target);
  if (pending.length > 0) {
    skipped.push({
      number: issue.number,
      target,
      status: "blocked",
      detail: `waiting on ${pending.map((n) => `#${n}`).join(", ")}`,
    });
    continue;
  }
  plans.push({ issue, target });
}

if (DRY_RUN) {
  console.log("\n[dry-run] dispatch plan:");
  for (const plan of plans) {
    console.log(`  #${plan.issue.number} "${plan.issue.title}" -> ${plan.target}`);
  }
  printSummary(skipped);
  process.exit(0);
}

if (plans.length === 0) {
  console.log("\nEvery ready-for-agent issue is blocked. Nothing to dispatch this run.");
  printSummary(skipped);
  process.exit(0);
}

const settled = await Promise.allSettled(plans.map(runIssue));

const dispatched: Outcome[] = settled.map((entry, index) => {
  const plan = plans[index]!;
  if (entry.status === "rejected") {
    return {
      number: plan.issue.number,
      target: plan.target,
      status: "failed",
      detail: errorMessage(entry.reason),
    };
  }
  const { branch, result } = entry.value;
  if (result.commits.length === 0) {
    return {
      number: plan.issue.number,
      target: plan.target,
      status: "skipped",
      detail: "agent produced no commits",
    };
  }
  // Open a PR only when the agent signaled completion. A missing
  // completionSignal means it stopped before passing its gates (or hit the
  // iteration limit), so its commits are partial. Leave the branch for review
  // instead of opening a red PR.
  if (!result.completionSignal) {
    return {
      number: plan.issue.number,
      target: plan.target,
      status: "incomplete",
      detail: `agent did not signal completion; ${result.commits.length} commit(s) left on ${branch} for review`,
    };
  }
  return openPullRequest(plan, branch, result.commits.length);
});

printSummary([...dispatched, ...skipped]);
