import json
import requests
from config import url
import pytest
from tests.http.fixtures import test_app

@pytest.mark.skip(reason="post req needs to be changed")
def test_xmlNotFound():

    token = create_user()

    print("token" + token)
    print("xml not found test")

    with open('', 'rb') as new_file:
    
        file = {'file': new_file}
        response = requests.post(f"{url}sendInvoice",  headers={
                                'token': token}, files=file,)
        assert json.loads(response)['sentMail'] == False
        assert json.loads(response)['xmlFound'] == False
        print(response.text)

@pytest.mark.skip(reason="post req needs to be changed")
def test_xmlTooBig():

    token = create_user()

    print("token" + token)
    print("xml too big test")

    with open('', 'rb') as new_file:
    
        file = {'./tests/files/10MB_Test': new_file}
        response = requests.post(f"{url}sendInvoice",  headers={
                                'token': token}, files=file,)
        assert json.loads(response)['sentMail'] == False
        assert json.loads(response)['xmlRightSize'] == False
        print(response.text)

@pytest.mark.skip(reason="post req needs to be changed")
def test_invalidEmail():

    token = create_user()

    print("token" + token)
    print("invalid email test")

    with open('./tests/files/InvalidEmail.xml', 'rb') as new_file:
    
        file = {'file': new_file}
        response = requests.post(f"{url}sendInvoice",  headers={
                                'token': token}, files=file,)
        assert json.loads(response)['sentMail'] == False
        assert json.loads(response)['emailValid'] == False
        print(response.text)

@pytest.mark.skip(reason="no way of currently testing this")
def test_emailNotSent():

    token = create_user()

    print("token" + token)
    print("email not sent test")
    with test_app.test_client() as app:
        with open('./tests/files/ValidEmailNotSent.xml', 'rb') as file:

            response = app.post("/sendInvoice",  headers={
                                'token': token}, data = {
                                "file" : (file, "invoice.xml")
                                })
            assert json.loads(response.data)['sentMail'] == False
            print(response.data)


def create_user():
    with test_app.test_client() as app:
        resp = app.post("/createNewUser",
                             json={
                                 "email": "tayleung@email.com",
                                 "username": "tayleung",
                                 "password": "password"})
        resp = app.post("/newSession",
                             json={
                                 "username": "tayleung",
                                 "password": "password"})

    assert resp.status_code == 200

    return json.loads(resp.data)['token']
