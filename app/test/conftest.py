import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.config.app_config import settings

@pytest.fixture
def client():
    """테스트 클라이언트 생성"""
    return TestClient(
        app = app,
        base_url = f"http://testserver:{settings.APP_PORT}{settings.API_PREFIX}"
        )