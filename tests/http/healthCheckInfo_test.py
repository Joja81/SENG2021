import requests
from config import url
from tests.http.fixtures import test_app

def test_healthInfo():
    with test_app.test_client() as app:
        response = app.get("/healthCheck")
        assert response.status_code == 200