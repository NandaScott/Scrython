# Contributing

If you'd like to contribute something to the project you are more than welcome to. Here's some guidelines to streamline the process.

## Development Environment Setup

### Requirements

- **Python 3.10 or higher** (required for modern type hints)
- Git

### Initial Setup

1. **Fork and clone the repository:**

   - First, fork the repository on GitHub by clicking the "Fork" button at https://github.com/NandaScott/Scrython
   - Then clone your fork:

   ```bash
   git clone https://github.com/YOUR_USERNAME/Scrython.git
   cd Scrython
   ```

   - Add the upstream repository as a remote:

   ```bash
   git remote add upstream https://github.com/NandaScott/Scrython.git
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**

   - On Linux/Mac:
     ```bash
     source venv/bin/activate
     ```
   - On Windows:
     ```bash
     venv\Scripts\activate
     ```

4. **Install Scrython with development dependencies:**

   ```bash
   pip install -e .[dev]
   ```

   This installs:

   - `black` - Code formatter
   - `ruff` - Fast Python linter
   - `mypy` - Static type checker
   - `pytest` - Testing framework
   - `pytest-cov` - Code coverage reporting
   - `pre-commit` - Git hook framework

5. **Set up pre-commit hooks (recommended):**

   ```bash
   pre-commit install
   ```

   This ensures code is automatically formatted and linted before each commit.

## Running Tests

### Basic Test Commands

```bash
# Run the full test suite
pytest

# Run with verbose output
pytest -v

# Run a specific test file
pytest tests/test_cards.py

# Run a specific test function
pytest tests/test_cards.py::test_card_named

# Run tests with coverage report
pytest --cov=scrython --cov-report=html
```

### Test Markers

Tests are marked with categories for selective execution:

```bash
# Run only fast tests (skip slow ones)
pytest -m "not slow"

# Run only integration tests
pytest -m integration
```

### Coverage Reports

After running tests with coverage, open `htmlcov/index.html` in your browser to view detailed coverage information.

## Code Quality Tools

### Black (Code Formatter)

Black automatically formats code to a consistent style:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .

# Format a specific file
black scrython/cards/cards.py
```

### Ruff (Linter)

Ruff checks for code quality issues and common mistakes:

```bash
# Lint all files
ruff check .

# Auto-fix issues where possible
ruff check . --fix

# Lint a specific file
ruff check scrython/cards/cards.py
```

### Mypy (Type Checker)

Mypy verifies type hints and catches type-related bugs:

```bash
# Type check the entire codebase
mypy scrython

# Type check a specific file
mypy scrython/cards/cards.py
```

### Pre-commit Hooks

If you installed pre-commit hooks, they'll run automatically on `git commit`. To run manually:

```bash
# Run all hooks on staged files
pre-commit run

# Run all hooks on all files
pre-commit run --all-files

# Run a specific hook
pre-commit run black --all-files
```

## Project Architecture

Scrython uses a **request handler + mixins** pattern to compose API endpoint classes.

### Core Components

1. **`scrython/base.py`**: Contains `ScrythonRequestHandler` - the base class for all API requests

   - `_build_path()`: Resolves endpoint path parameters (e.g., `:id`, `:code`)
   - `_build_params()`: Constructs query parameters
   - `_fetch()`: Executes HTTP request and handles errors via `ScryfallError`

2. **Mixins** (`base_mixins.py` and module-specific `*_mixins.py` files):

   - Provide `@property` accessors to the `scryfall_data` dictionary
   - Examples:
     - `ScryfallListMixin`: For endpoints returning lists (search results, collections)
     - `CoreFieldsMixin`, `GameplayFieldsMixin`, `PrintFieldsMixin`: Card-specific data accessors

3. **Factory Classes**: `Cards`, `Sets`, `BulkData`
   - Use `__new__()` to dynamically instantiate the correct endpoint class based on kwargs
   - Example: `Cards(fuzzy="Lightning")` returns `CardsNamed`, while `Cards(search="bolt")` returns `CardsSearch`

### Module Structure

```
scrython/
├── base.py              # ScrythonRequestHandler, ScryfallError
├── base_mixins.py       # ScryfallListMixin, ScryfallCatalogMixin
├── utils.py             # Utility functions
├── cards/
│   ├── cards.py         # Card endpoint classes + Cards factory
│   └── cards_mixins.py  # Card data accessors
├── sets/
│   ├── sets.py          # Set endpoint classes + Sets factory
│   └── sets_mixins.py   # Set data accessors
└── bulk_data/
    ├── bulk_data.py     # Bulk data endpoint classes + BulkData factory
    └── bulk_data_mixins.py  # Bulk data accessors
```

### Adding New Endpoints

1. Add endpoint class in the appropriate module (e.g., `scrython/cards/cards.py`)
2. Set `_endpoint` class variable with path template (use `:param` for path parameters)
3. Inherit from `ScrythonRequestHandler` + appropriate mixins
4. Update factory class's `__new__()` method to route to your endpoint
5. Add new properties to mixin files if Scryfall returns new fields

### Adding New Tests

1. Create or update test files in the `tests/` directory
2. Follow the naming convention: `test_*.py` for files, `test_*` for functions
3. Use pytest fixtures defined in `conftest.py` for common test setup
4. Mock Scryfall API responses to avoid network calls in tests

## Branching Strategy

### Current Branch Structure

- **`main`**: Stable branch distributed to PyPI
- **`develop`**: Active development branch for new features and improvements
- **Feature branches**: Create from `develop` for new features

### Workflow

1. **Sync your fork with upstream:**

   ```bash
   git checkout develop
   git fetch upstream
   git merge upstream/develop
   ```

2. **Create a feature branch:**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes and commit:**

   ```bash
   # Pre-commit hooks will run automatically
   git add .
   git commit -m "Add feature description"
   ```

4. **Push to your fork:**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Create a pull request:**
   - Go to your fork on GitHub
   - Click "Compare & pull request"
   - Ensure the base repository is `NandaScott/Scrython` and the base branch is `develop` (or `main` for urgent hotfixes only)
   - Fill out the PR template and submit

## Code Style Guidelines

The primary goal is to make code easy to read and maintain. Follow these guidelines to ensure consistency across the codebase:

### Variable Naming

- **Use descriptive variable names** - avoid single character variables
- **Exceptions**: `f` for file operations, `i` for loop iterations
- **Examples**:
  - Good: `card_name`, `search_query`, `endpoint_url`
  - Avoid: `x`, `tmp`, `data` (unless contextually clear)

### Comments

- **Explain complex logic** - if code uses complex patterns (regex, algorithms), add a comment explaining what it does
- **Explain the "why", not the "what"** - if code does something unexpected, explain why it's necessary
- **Avoid redundant comments** - don't state the obvious (e.g., `# end for loop`, `# increment i`)
- **Example**:
  ```python
  # Use walrus operator to avoid double dictionary lookup
  if data_param := kwargs.get('data', None):
      data = json.dumps(data_param).encode('utf-8')
  ```

### Formatting

- **Indentation**: 4 spaces (enforced by Black)
- **Line length**: 100 characters (enforced by Black)
- **Imports**: Organized by type (standard library, third-party, local) using isort via Ruff

### Type Hints

- **Use modern Python 3.10+ syntax**:
  - Use `X | Y` instead of `Union[X, Y]`
  - Use `list[str]` instead of `List[str]`
  - Use `dict[str, Any]` instead of `Dict[str, Any]`
  - Use `str | None` instead of `Optional[str]`
- **Add type hints to function signatures** - parameters and return types
- **Use `Any` when necessary** - don't force incorrect types for dynamic data

### Code Quality

All code is automatically checked by pre-commit hooks. Ensure your code passes:

- Black formatting
- Ruff linting
- Mypy type checking (where applicable)

## AI-Assisted Contributions

I am not against using AI tools to help write code or tests. I use them myself. What I do object to is unreviewed AI output landing in the project.

If you used an LLM, an agent, or any AI tool to help write your contribution, the following rules apply.

### Expectations

- **You are the author, not the LLM.** Read every line. Run the tests yourself. Reproduce the bugs you claim to have fixed. If you cannot explain why a specific design choice was made, that section is not ready for review.
- **Write the PR description yourself.** A description that reads as LLM-generated is a strong signal that the rest of the PR was not reviewed by you either. Keep it short, plain, and in your own words. State what changed, why, and how you tested it.
- **Keep the scope reviewable.** This is a volunteer project. Split work into the smallest useful unit. If you have supporting research, link it externally rather than committing it.
- **Do not commit scratch work.** Exploratory scripts, prompt logs, and notes from your local workflow do not belong in the repo. The repo is for code that ships and the tests that cover it.
- **Run the project's quality bar before requesting review.** `pytest`, `ruff check`, `mypy`, and `black --check` should all be clean. If you used AI to write the code, you are responsible for running these against the output and fixing what the AI got wrong.

### What I will do if a PR looks unreviewed by a human

I'll close it. The PR description is usually the first signal. If the prose reads as LLM-written and the diff is large, I am not going to take on a free review for code the author did not read. I would rather you came back with something small and clearly your own.

### Out of scope regardless of how it was written

Reverse-engineered or undocumented Scryfall endpoints. Scrython tracks the [published Scryfall API](https://scryfall.com/docs/api). If a feature requires probing an internal endpoint, it does not belong here, regardless of how clean the implementation is.

## Before Submitting

Before submitting a pull request, ensure:

- [ ] All tests pass: `pytest`
- [ ] Code is formatted: `black .`
- [ ] No linting errors: `ruff check .`
- [ ] Type checking passes: `mypy scrython`
- [ ] Pre-commit hooks pass: `pre-commit run --all-files`
- [ ] New features have tests
- [ ] Documentation is updated if needed

## Thank you

I'd like to thank you for taking an interest in contributing to Scrython. I'm not always able to work on this and can't keep it maintained all the time, even as Scryfall updates its API.
