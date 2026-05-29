FROM python:3.12-bookworm

# Install system dependencies
RUN apt-get update && apt-get install -y \
  git \
  curl \
  jq \
  && rm -rf /var/lib/apt/lists/*

# Install GitHub CLI
RUN curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg \
  | dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg \
  && echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" \
  | tee /etc/apt/sources.list.d/github-cli.list > /dev/null \
  && apt-get update && apt-get install -y gh \
  && rm -rf /var/lib/apt/lists/*

# Build-args for UID/GID alignment: sandcastle docker build-image
# defaults these to the host user's UID/GID so image-built files
# and bind-mounted files share an owner without runtime chown.
ARG AGENT_UID=1000
ARG AGENT_GID=1000

# The python base image has no unprivileged user, so create "agent"
# with the host's UID/GID for clean ownership on the bind-mounted worktree.
RUN groupadd -o -g $AGENT_GID agent \
  && useradd -o -u $AGENT_UID -g $AGENT_GID -m -d /home/agent -s /bin/bash agent
USER ${AGENT_UID}:${AGENT_GID}

# Install uv (used for fast dependency installs) into the agent's local bin.
RUN curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Claude Code CLI
RUN curl -fsSL https://claude.ai/install.sh | bash

# Add uv and Claude to PATH
ENV PATH="/home/agent/.local/bin:$PATH"

WORKDIR /home/agent

# In worktree sandbox mode, Sandcastle bind-mounts the git worktree at /home/agent/workspace
# and overrides the working directory to /home/agent/workspace at container start.
# Structure your Dockerfile so that /home/agent/workspace can serve as the project root.
ENTRYPOINT ["sleep", "infinity"]
