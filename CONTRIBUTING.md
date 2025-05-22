# Contributing to Cheatos

Welcome! Whether you're fixing a bug, proposing a feature, or just improving docs, your help is appreciated.

---

## Getting Started

1. **Fork the repo** and clone your fork:
   ```bash
   git clone https://github.com/Gorbiel/Cheatos.git
   cd cheatos
   ```

2. **Set up the environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements-dev.txt
   ```

3. **Install Cheatos locally in editable mode (optional but recommended)**:
   ```bash
   pip install -e .
   ```

---

## Running Tests

Run the test suite:

```bash
pytest
```

---

## Linting

Check code style using `pylint`:

```bash
pylint $(git ls-files '*.py')
```

(We use a PEP8-ish style. Feel free to generate a `.pylintrc` file and suggest changes.)

---

## Submitting a Pull Request

- Create a new branch:  
  ```bash
  git checkout -b my-feature
  ```

- Make your changes with clear, focused commits.
- Ensure your code:
  - Passes tests
  - Passes linting
  - Adds tests if needed
  - Updates the README or docs if behavior changes

- Push and open a Pull Request to `main` with a clear title and description.

---

##  Communication & Feedback

- Use GitHub Issues to report bugs or suggest features.
- Tag your PRs with labels like `type: bug`, `type: feature`, etc.
- Keep a respectful tone — see our [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Unsure Where to Start?

Look for issues labeled `good first issue` or `help wanted`.

You can also suggest new cheato features or UX improvements — CLI ergonomics are a big part of this project.

---

## Packaging

We use [build](https://pypi.org/project/build/) and [twine](https://pypi.org/project/twine/) for PyPI releases.

To build locally:

```bash
python -m build
twine check dist/*
```

---

All contributions are welcome.
