import json
from config import url
import pytest
from tests.http.fixtures import test_app

def test_xmlNotFound():

    with test_app.test_client() as app:

        token = create_user(app)

        print("token" + token)
        print("xml not found test")

        response = app.post("sendInvoice",  headers={
                                'token': token},)
        assert json.loads(response.data)['sentMail'] == False
        assert json.loads(response.data)['xmlFound'] == False
        print(response.data)

def test_xmlTooBig():
    with test_app.test_client() as app:

        token = create_user(app)

        print("token" + token)
        print("xml too big test")

        with open('./tests/files/10mb_test.txt', 'rb') as new_file:

            file = {'file': new_file}
            response = app.post("sendInvoice",  headers={
                                    'token': token}, data = {
                                        "file" : (file, "invoice.xml")
                                        },)
            assert json.loads(response.data)['sentMail'] == False
            assert json.loads(response.data)['xmlRightSize'] == False
            print(response.data)

def test_invalidEmail():

    with test_app.test_client() as app:

        token = create_user(app)

        print("token" + token)
        print("invalid email test")

        with open('./tests/files/InvalidEmail.xml', 'rb') as new_file:

            file = {'file': new_file}
            response = app.post("sendInvoice",  headers={
                                    'token': token}, data = {
                                        "file" : (file, "invoice.xml")
                                        },)
            assert json.loads(response.data)['sentMail'] == False
            assert json.loads(response.data)['emailValid'] == False
            print(response.data)

def create_user(app):
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
