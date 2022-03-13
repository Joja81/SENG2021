import json
import os
from io import BytesIO
import werkzeug
from config import url
from tests.http.fixtures import test_app
from werkzeug.datastructures import FileStorage, FileMultiDict
i = 0


def test_invalid_auth():
    with test_app.test_client() as app:
        response = app.post("/sendInvoice",  headers={
                                    'token': "Hello"}, data = {
                                        "file" : (open('./tests/files/AUInvoice.xml', 'rb'), "invoice.xml")
                                        })
        assert response.status_code == 403


def test_basic():
    with test_app.test_client() as app:
        token = create_user()

        print("token" + token)
        response = app.post("/sendInvoice",  headers={
                                    'token': token}, data = {
                                        "file" : (open('./tests/files/AUInvoice.xml', 'rb'), "invoice.xml")
                                        })
            
        print(response.data)
        assert response.status_code == 200


def create_user():
    with test_app.test_client() as app:
        app.post("/createNewUser",
                  json={
                      "email": f"email{i+100}@email.com",
                      "username": f"Username{i+100}",
                      "password": "password"})

        resp = app.post("/newSession", 
                    json={'username': "Username4",
                        'password': "password"})

    assert resp.status_code == 200

    return json.loads(resp.data)['token']
