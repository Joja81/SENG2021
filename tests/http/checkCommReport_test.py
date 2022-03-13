import json
import requests
from config import url


def xmlNotFound():

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


def xmlTooBig():

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


def invalidEmail():

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


def emailNotSent():

    token = create_user()

    print("token" + token)
    print("email not sent test")

    with open('./tests/files/ValidEmailNotSent.xml', 'rb') as new_file:
    
        file = {'file': new_file}
        response = requests.post(f"{url}sendInvoice",  headers={
                                'token': token}, files=file,)
        assert json.loads(response)['sentMail'] == False
        print(response.text)


def create_user():
    requests.post(url + "createNewUser",
                  json={
                      "email": f"tayleung@email.com",
                      "username": f"tayleung",
                      "password": "password"})

    resp = requests.post(
        url + "newSession", json={'username': "tayleung", 'password': "password"})

    assert resp.status_code == 200

    return json.loads(resp.text)['token']
