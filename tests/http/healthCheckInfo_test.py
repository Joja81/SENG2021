import json
from config import url
from tests.http.fixtures import test_app

def test_healthInfo():
    with test_app.test_client() as app:
        resp = app.get("/healthCheck")
        data = json.loads(resp.data)

        assert data['alive']
        assert data['serverUpTime'] > 0
        assert data['numTransactions'] >= 0