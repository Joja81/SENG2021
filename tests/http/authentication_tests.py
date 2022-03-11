from config import url
import requests

# Testing for createNewUser

def test_invalid_email():

    response = requests.post(
        url + "/createNewUser",
        json={"email": "email",
              "username": "username",
              "password": "password"})

    assert response.status_code == 400


def test_invalid_username():
    
    # Too short username
    
    response = requests.post(url + "/createNewUser",
                             json={
                                 "email": "email@email.com",
                                 "username": "1234",
                                 "password": "password"})

    assert response.status_code == 400
    
    #Too long username

    response = requests.post(url + "/createNewUser",
                             json={"email": "email@email.com",
                                   "username": "24321432142341234123412341234123lk4j123l4j1l32jd41kl;3d4j12lk;3d4j12l3d4;kj12l3;d41j2k;l3d4j123lk;d4j",
                                   "password": "password"})

    assert response.status_code == 400

def test_invalid_password():
    # Too short password
    
    response = requests.post(url + "/createNewUser",
                             json={
                                 "email": "email@email.com",
                                 "username": "username",
                                 "password": "1234"})

    assert response.status_code == 400
    
    #Too long password

    response = requests.post(url + "/createNewUser",
                             json={"email": "email@email.com",
                                   "username": "username",
                                   "password": "24321432142341234123412341234123lk4j123l4j1l32jd41kl;3d4j12lk;3d4j12l3d4;kj12l3;d41j2k;l3d4j123lk;d4j"})

    assert response.status_code == 400

def test_duplicate_email():
    response = requests.post(url + "/createNewUser",
                             json={
                                 "email": "email@email.com",
                                 "username": "Username",
                                 "password": "password"})

    assert response.status_code == 200
    
    response = requests.post(url + "/createNewUser",
                             json={
                                 "email": "email@email.com",
                                 "username": "Username",
                                 "password": "password"})

    assert response.status_code == 400

def test_working():
    response = requests.post(url + "/createNewUser",
                             json={
                                 "email": "email@email.com",
                                 "username": "Username",
                                 "password": "password"})

    assert response.status_code == 200
    
    assert response.json == {"success" : True}