Contributing to SATA / ATAS
================================

Thanks for your interest in contributing!
This project welcomes code, documentation, tests, and issue reports. By
participating, you agree to keep a respectful, collaborative environment.

----------------------------------------
Ways to contribute
----------------------------------------
- Fix bugs or improve code quality
- Add tests (unit or integration)
- Improve docs / README / examples
- Propose or implement new features
- Report issues with a minimal reproducible example

----------------------------------------
Getting started (local dev)
----------------------------------------
1) Clone your fork
   git clone https://github.com/<your-user>/SATA.git
   cd SATA

2) (Optional but recommended) create a virtualenv
   python -m venv .venv
   # Linux/macOS:
   source .venv/bin/activate
   # Windows (PowerShell):
   # .venv\Scripts\Activate.ps1

3) Install dependencies
   pip install -r requirements.txt

4) Install test tooling (dev)
   pip install -U pytest

Running the test suite
----------------------
pytest

Note: The project uses a pytest.ini with pythonpath = src,
so imports such as 'import processamento.filtro_texto' work without installing
the package.

Important: Avoid downloading or loading heavy resources (e.g., spaCy models)
at import time. Load them inside functions so imports and CI are fast and
reliable.

----------------------------------------
Project layout
----------------------------------------
src/
  gui.py
  main.py
  processamento/
    __init__.py
    filtro_texto.py
    converter_tabela.py
    identificador_sexo.py
    estatisticas_texto.py
tests/
  test_basic.py

- Source code lives under 'src/'.
- Tests live under 'tests/' and are executed with pytest.
- Keep imports consistent with the current layout, e.g.:
    import processamento.filtro_texto
    # or
    from processamento.filtro_texto import filtrar_texto

----------------------------------------
Code style & quality
----------------------------------------
- Follow PEP 8 (you may use flake8 or ruff locally).
- Add docstrings (Google or NumPy style) to public functions/classes.
- Prefer small, well-named functions with type hints when useful.
- Do not run heavy I/O or model downloads at module import.

----------------------------------------
Submitting changes (Pull Requests)
----------------------------------------
1. Fork the repo and create a topic branch from 'main'.
2. Make your changes (please add/update tests when applicable).
3. Run the test suite locally:
   pytest
4. Commit with clear messages that explain the what and why.
5. Open a Pull Request:
   - Describe the motivation and behavior changes.
   - Reference related issues if applicable.

PR checklist
------------
- [ ] Code builds and tests pass locally (pytest)
- [ ] New/changed behavior is covered by tests
- [ ] Docs/README updated if needed

----------------------------------------
Reporting issues
----------------------------------------
Use the GitHub Issues tab. When possible, include:
- OS and Python version
- Steps to reproduce (minimal example)
- Expected vs. actual behavior
- Error messages / stack traces

----------------------------------------
License
----------------------------------------
By contributing, you agree that your contributions will be licensed under the
project’s license (see 'LICENSE').
