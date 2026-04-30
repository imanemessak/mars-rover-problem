# Mars Rover Problem 🚀

## Goals

The aim of this project is to solve the classic NASA Mars Rover kata using
Python and Object-Oriented Programming principles. It demonstrates clean
architecture (Single Responsibility), thorough test coverage, and a
production-ready CI pipeline.

## Overview

### Language & Stack

[![Made with Python](https://img.shields.io/badge/Made%20with-Python%203.11+-blue?logo=python)](https://www.python.org/)
[![Tested with pytest](https://img.shields.io/badge/Tested%20with-pytest-blue?logo=pytest)](https://pytest.org/)
[![Linted with Ruff](https://img.shields.io/badge/Linted%20with-Ruff-blue)](https://docs.astral.sh/ruff/)
[![CI](https://github.com/imanemessak/mars-rover-problem/actions/workflows/ci.yml/badge.svg)](https://github.com/imanemessak/mars-rover-problem/actions/workflows/ci.yml)

### Questions

[:speech_balloon: Ask a question](https://github.com/imanemessak/mars-rover-problem/issues/new)
[:book: Read the questions](https://github.com/imanemessak/mars-rover-problem/issues/)

**Contribution**

[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-v2.0%20adopted-ff69b4.svg)](CODE_OF_CONDUCT.md)

---

## Problem Statement

A squad of robotic rovers are landed by NASA on a rectangular plateau on Mars.
Each rover's position is represented by `x y HEADING` (e.g. `1 2 N`). NASA
sends a string of instructions: `L` (turn left), `R` (turn right), `M` (move
forward one grid point).

**Test Input:**
```
5 5        ← plateau upper-right corner
1 2 N      ← rover initial position
LMLMLMLMM  ← instructions
3 3 E
MMRMMRMRRM
```


**Expected Output:**
```
1 3 N
5 1 E
```

---

## Architecture

```
src/mars_rover/
├── plateau.py    # Plateau — grid boundary validation
├── rover.py      # Rover   — movement & rotation logic
├── mission.py    # Mission — input parsing & sequential orchestration
└── __main__.py   # CLI entry point
```

Each class has a single responsibility. Dependency flow is strictly one-directional:

```
Mission → creates → Plateau
Mission → creates → Rover (with Plateau injected)
Rover   → validates bounds via → Plateau
```

---


---

## Setup

Make sure you have Python 3.10+ installed, then:

```bash
# Clone the repository
git clone https://github.com/imanemessak/mars-rover-problem.git
cd mars-rover-problem

# Create and activate a virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

---

## Run

```bash
# Run against an input file
python -m mars_rover examples/input.txt

# Or using the installed CLI command
mars-rover examples/input.txt
```

---

## Docker

```bash
# Pull the latest image
docker pull ghcr.io/imanemessak/mars-rover-problem:latest

# Run against a local input file
docker run --rm -v $(pwd)/examples:/data \
  ghcr.io/imanemessak/mars-rover-problem:latest /data/input.txt
```

---

## Test

```bash
# Run all tests
pytest

# Run with coverage report
pytest --cov=mars_rover --cov-report=term-missing

# Run a specific test file
pytest tests/test_rover.py -v
```

The test suite covers **55 cases** across three files:

| File | Scope |
|---|---|
| `test_plateau.py` | Boundary validation, construction errors, parametrized coordinates |
| `test_rover.py` | Turning, moving, acceptance tests, edge cases, error cases |
| `test_mission.py` | Parsing, sequential execution, whitespace tolerance, file I/O |

---

## Lint

```bash
ruff check src/ tests/
```

---

## CI

GitHub Actions runs on every push and pull request to `main` / `dev`.

| Job | Tool | Trigger |
|---|---|---|
| 💎 Quality | Ruff lint + format check | all branches |
| 🛡️ Security | Bandit (SAST) + Safety (CVEs) | all branches |
| 🤖 Tests | pytest + Codecov (Python 3.11, 3.12, 3.13) | after quality |
| 🛠️ Build | wheel + sdist verified with Twine | after tests + security |
| 🐳 Docker | build & push to ghcr.io | after build |
| 📤 Release | python-semantic-release | after build, `main` only |

See [`.github/workflows/ci.yml`](.github/workflows/ci.yml).

---

## Contributing

Please see the [CONTRIBUTING](CONTRIBUTING.md) file.

## Contributor Code of Conduct

Please note that this project is released with a
[Contributor Code of Conduct](https://www.contributor-covenant.org/).
By participating in this project you agree to abide by its terms.
See [CODE_OF_CONDUCT](CODE_OF_CONDUCT.md).

## Licence

This work is licensed under a
[Creative Commons Attribution-ShareAlike 4.0 International License][cc-by-sa].

[![CC BY-SA 4.0][cc-by-sa-image]][cc-by-sa]

[cc-by-sa]: http://creativecommons.org/licenses/by-sa/4.0/
[cc-by-sa-image]: https://licensebuttons.net/l/by-sa/4.0/88x31.png