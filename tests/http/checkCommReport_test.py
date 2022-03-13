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
        print(response.text)


def xmlTooBig():

    token = create_user()

    print("token" + token)
    print("xml too big test")

    with open('', 'rb') as new_file:
    
        file = {'./tests/files/10MB_Test': new_file}
        response = requests.post(f"{url}sendInvoice",  headers={
                                'token': token}, files=file,)
        print(response.text)


def invalidEmail():

    token = create_user()

    print("token" + token)
    print("invalid email test")

    with open('./tests/files/InvalidEmail.xml', 'rb') as new_file:
    
        file = {'file': new_file}
        response = requests.post(f"{url}sendInvoice",  headers={
                                'token': token}, files=file,)
        print(response.text)


def emailNotSent():

    token = create_user()

    print("token" + token)
    print("email not sent test")

    with open('./tests/files/ValidEmailNotSent.xml', 'rb') as new_file:
    
        file = {'file': new_file}
        response = requests.post(f"{url}sendInvoice",  headers={
                                'token': token}, files=file,)
        print(response.text)


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
