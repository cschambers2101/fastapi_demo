# fastapi_demo

A small FastAPI and SQLModel demo API for students, backed by SQLite.

## Dev

- Setup: `python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt`
- Test command: `pytest`
- Coverage command: `pytest --cov=basic_api --cov-report=term-missing`
- Coverage target: 80% overall. New code is covered in full.
- Security audit command: `pip-audit -r requirements.txt && bandit -q basic_api.py`
- Dev environment: none. A local run stands in for dev (agreed by Craig, 24 November 2026).
- Dev deploy command: none. Start the app locally with `uvicorn basic_api:app --port 8000`.
- Dev test command: `pytest`, then the feature's own check with `curl` against `http://localhost:8000`.
- Production environment: none.
- Branches: `beta` deploys to dev. `main` changes only at a release.
