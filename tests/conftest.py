import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine

# Make basic_api importable from the repository root
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest.fixture
def client(tmp_path, monkeypatch):
    ''' A TestClient backed by a temporary SQLite database, not database.db'''
    # basic_api creates database.db in the working directory on import,
    # so import it from inside a temporary directory
    monkeypatch.chdir(tmp_path)
    import basic_api

    test_engine = create_engine(f"sqlite:///{tmp_path / 'test.db'}")
    SQLModel.metadata.create_all(test_engine)
    monkeypatch.setattr(basic_api, "engine", test_engine)

    with TestClient(basic_api.app) as test_client:
        yield test_client

    test_engine.dispose()
