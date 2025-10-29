# Contributing to SATA / ATAS

Thanks for your interest in contributing!

This project welcomes code, documentation, tests, and issue reports. By
participating, you agree to keep a respectful, collaborative environment.

---

## Ways to contribute

- Fix bugs or improve code quality
- Add tests (unit or integration)
- Improve docs / README / examples
- Propose or implement new features
- Report issues with a minimal reproducible example

---

## Getting started (local dev)

```bash
# 1) Clone your fork
git clone https://github.com/<your-user>/SATA.git
cd SATA

# 2) (Optional but recommended) create a virtualenv
python -m venv .venv
# Linux/macOS:
source .venv/bin/activate
# Windows (PowerShell):
# .venv\Scripts\Activate.ps1

# 3) Install dependencies
pip install -r requirements.txt

# 4) Install test tooling (dev)
pip install -U pytest
