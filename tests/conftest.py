import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.storage import job_store


@pytest.fixture()
def client():
    job_store.clear()
    return TestClient(app)
