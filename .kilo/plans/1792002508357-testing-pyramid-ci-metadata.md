# Testing Pyramid, CI, and Package Metadata Plan

## Project Context
- **Project**: `pythonesque` - offline deterministic absurdist title generator
- **Current state**: 6 unit tests only, no CI, basic pyproject.toml
- **Target**: Full testing pyramid + GitHub Actions CI + complete package metadata

---

## 1. Testing Pyramid Implementation

### Unit Tests (`tests/unit/`)
**Target: ~15-20 tests** - Test individual methods in isolation

| Module | Methods to Test | Test Cases |
|--------|----------------|------------|
| `generator.py` | `_generate_historical_ordinal()` | 1st/2nd/3rd/4th/11th/12th/13th/21st suffixes |
| | `_build_proper_noun()` | Title/first/last combinations, nickname insertion, double-barrel surnames |
| | `_resolve()` - each token type | `historical_ordinal`, `generated_proper_noun`, `enhanced_institution`, `generated_legal_action`, `generated_natural_philosophy_axiom`, `generated_academic_body`, `generated_logistics_action`, `generated_academic_discipline`, `noun_verbing` |
| | `_expand()` | Nested token resolution, no tokens, multiple tokens |
| | `_join()` | Empty parts filtering, normal joining |
| | `_fix_indefinite_articles()` | Vowel sounds, consonant sounds, edge cases |
| | `_slugify()` | Basic, Unicode, symbols, length limit, hyphen normalization |

### Integration Tests (`tests/integration/`)
**Target: 5-8 tests** - Test grammar resolution pipeline

| Feature | Test Cases |
|---------|------------|
| Template expansion | All START templates resolve without unresolved `{{}}` |
| Complex template chains | Legal templates (3-part), Academic (2-part), Sports (2-part), Historical competition (3-part) |
| Modular components | Historical competition prefix/middle/suffix, Legal authority/location/framework, Academic title/affiliation, Sports events |
| Slugify integration | Generated titles produce valid slugs (lowercase, alnum+hyphen, no leading/trailing hyphens) |
| Determinism | Same seed → identical sequence across multiple generator instances |
| Complexity filtering | Exact match, range match, invalid fallback |

### E2E Tests (`tests/e2e/`)
**Target: 8-12 tests** - Test CLI entry point (`src/pythonesque/cli.py`)

| CLI Feature | Test Cases |
|-------------|------------|
| Basic generation | Default seed, count=1, plain text output |
| Seed reproducibility | `-s "custom"` produces same output across invocations |
| Multiple titles | `-c 5` produces 5 titles |
| Unique flag | `-u` with count generates unique titles |
| Slugify output | `-g` produces `(title, slug)` tuples |
| Complexity filter | `-x 3` exact, `-x 2-4` range |
| No-leading-the | `-n` strips leading "The " |
| Output formats | `-f json`, `-f csv`, `-f tsv` with/without slugify |
| Version flag | `--version` prints version and exits |
| Error handling | Invalid complexity, negative count, mutually exclusive formats |

---

## 2. CI Pipeline (GitHub Actions)

### Workflow File: `.github/workflows/ci.yml`

**Jobs:**
1. **lint** - `ruff check .` + `ruff format --check .`
2. **typecheck** - `mypy src/pythonesque` (or `pyright`)
3. **test** - Matrix: Python 3.10, 3.11, 3.12, 3.13, 3.14
   - Install deps: `pip install -e .[test]`
   - Run: `pytest --cov=src/pythonesque --cov-report=xml`
   - Upload coverage to Codecov (optional)
4. **coverage-check** - Fail if coverage < 80% (configurable)

**Triggers:** Push to main, PR to main

---

## 3. Pre-commit Hooks (`.pre-commit-config.yaml`)

```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.6.0
    hooks:
      - id: ruff
      - id: ruff-format
  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.11.0
    hooks:
      - id: mypy
        args: [--strict, src/pythonesque]
  - repo: local
    hooks:
      - id: pytest
        name: pytest
        entry: pytest
        language: system
        pass_filenames: false
        always_run: true
```

---

## 4. Package Metadata Updates (`pyproject.toml`)

### Add to `[project]`:

```toml
authors = [
  {name = "Michael Ron Bernstein", email = "zopemaven@gmail.com"}
]
maintainers = [
  {name = "Michael Ron Bernstein", email = "zopemaven@gmail.com"}
]
keywords = [
  "monty-python", "absurdist", "generator", "text-generator",
  "title-generator", "slugs", "cli", "deterministic", "humor"
]
classifiers = [
  "Development Status :: 4 - Beta",
  "Intended Audience :: Developers",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Programming Language :: Python :: 3 :: Only",
  "Programming Language :: Python :: 3.10",
  "Programming Language :: Python :: 3.11",
  "Programming Language :: Python :: 3.12",
  "Programming Language :: Python :: 3.13",
  "Programming Language :: Python :: 3.14",
  "Topic :: Software Development :: Libraries :: Python Modules",
  "Topic :: Utilities",
  "Environment :: Console",
]
urls = {
  "Homepage" = "https://github.com/webmaven/pythonesque",
  "Repository" = "https://github.com/webmaven/pythonesque",
  "Issues" = "https://github.com/webmaven/pythonesque/issues",
  "Documentation" = "https://webmaven.github.io/pythonesque/",
}
readme = {file = "README.adoc", content-type = "text/plain"}
license = {file = "LICENSE"}
requires-python = ">=3.10"
```

### Add dependencies:

```toml
[project.optional-dependencies]
dev = [
  "pytest>=8",
  "pytest-cov>=4",
  "ruff>=0.6",
  "mypy>=1.11",
  "pre-commit>=3.0",
]
```

---

## 5. Tool Configuration Files

### `ruff.toml` (or `[tool.ruff]` in pyproject.toml)
```toml
[tool.ruff]
target-version = "py310"
line-length = 100
select = ["E", "F", "I", "UP", "W"]
ignore = ["E501"]  # line too long (handled by formatter)
```

### `mypy.ini` (or `[tool.mypy]` in pyproject.toml)
```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
```

---

## 6. Directory Structure Changes

```
tests/
├── unit/
│   ├── test_generator_core.py      # _resolve, _expand, _join, helpers
│   ├── test_generator_tokens.py    # Each token type resolution
│   ├── test_slugify.py             # Slugify edge cases
│   └── test_articles.py            # _fix_indefinite_articles
├── integration/
│   ├── test_template_expansion.py  # All START templates resolve
│   ├── test_modular_templates.py   # Legal, academic, sports, historical
│   ├── test_determinism.py         # Seed reproducibility
│   └── test_complexity.py          # Complexity filtering
└── e2e/
    ├── test_cli_basic.py           # Basic generation, seeds, count
    ├── test_cli_formats.py         # JSON, CSV, TSV output
    ├── test_cli_flags.py           # -u, -g, -x, -n combinations
    └── test_cli_errors.py          # Error handling
```

---

## 7. Implementation Order

1. **Add tool configs** (ruff, mypy, pre-commit) to pyproject.toml
2. **Update package metadata** in pyproject.toml
3. **Create test directory structure** and add unit tests
4. **Add integration tests**
5. **Add E2E tests**
6. **Create GitHub Actions workflow**
7. **Create pre-commit config**
8. **Verify**: Run `pre-commit install`, `pytest`, `ruff check`, `mypy`

---

## 8. Validation Criteria

- [ ] All existing tests pass
- [ ] New unit tests cover all public/private methods in generator.py
- [ ] Integration tests verify full grammar resolution pipeline
- [ ] E2E tests cover all CLI flags and output formats
- [ ] CI runs on push/PR and passes on Python 3.10-3.14
- [ ] Coverage ≥ 80% (enforced in CI)
- [ ] Pre-commit hooks run locally and in CI
- [ ] Package metadata complete for PyPI publishing
- [ ] `pip install -e .[dev]` installs all dev dependencies