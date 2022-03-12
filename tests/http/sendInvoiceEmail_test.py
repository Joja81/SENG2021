from urllib import response
import pytest
import requests
from config import url

def invalid_auth():
    file = {'file': open('./tests/files/AUInvoice.xml', 'rb')}
    response = requests.post(f"{url}/sendInvoice", files=file, json = {'token' : "Hello"})
    assert response.status_code == 403

def test_basic():
    file = {'file': open('./tests/files/AUInvoice.xml', 'rb')}
    response = requests.post(f"{url}/sendInvoice", files=file)
    print(response.text)
    assert response.status_code == 200