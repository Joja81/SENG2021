import json
import requests
from config import url

i = 0


def test_invalid_auth():
    with open('./tests/files/AUInvoice.xml', 'rb') as new_file:
        file = {'file': new_file}
        response = requests.post(
            f"{url}sendInvoice", files=file, json={'token': "Hello"})
        assert response.status_code == 403


def test_basic():

    token = create_user()

    print("token" + token)

    with open('./tests/files/AUInvoice.xml', 'rb') as new_file:
    
        file = {'file': new_file}
        response = requests.post(f"{url}sendInvoice",  headers={
                                'token': token}, files=file,)
        print(response.text)
        assert response.status_code == 200


def create_user():
    requests.post(url + "createNewUser",
                  json={
                      "email": f"email{i+100}@email.com",
                      "username": f"Username{i+100}",
                      "password": "password"})

    resp = requests.post(
        url + "newSession", json={'username': "Username4", 'password': "password"})

    assert resp.status_code == 200

    return json.loads(resp.text)['token']
