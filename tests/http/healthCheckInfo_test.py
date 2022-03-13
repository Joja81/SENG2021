from urllib import response
import pytest
import requests
from config import url

def test_healthInfo():
    response = requests.get(f"{url}/healthCheck")
    assert response.status_code == 200