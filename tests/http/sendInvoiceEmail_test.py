from urllib import response
import pytest
import requests
from config import url

def test_basic():
    
    with open('./tests/files/AUInvoice.xml', 'rb') as new_file:
        file = {'file': new_file}
        response = requests.post(f"{url}/sendinvoice", files=file)
        print(response.text)
        assert response.status_code == 200