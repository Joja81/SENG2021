import json

from flask import request
from config import url
import requests
import pytest

'''
            ========================================================
                            createNewUser tests
            ========================================================
'''

# Testing for createNewUser

def test_invalid_email():

    resp = requests.post(
        url + "createNewUser",
        json={"email": "email",
              "username": "username",
              "password": "password"})

    assert resp.status_code == 400


def test_invalid_username():
    
    # Too short username
    resp = requests.post(url + "createNewUser",
                             json={
                                 "email": "email@email.com",
                                 "username": "1234",
                                 "password": "password"})

    assert resp.status_code == 400
    
    #Too long username
    resp = requests.post(url + "createNewUser",
                             json={"email": "email@email.com",
                                   "username": "24321432142341234123412341234123lk4j123l4j1l32jd41kl;3d4j12lk;3d4j12l3d4;kj12l3;d41j2k;l3d4j123lk;d4j",
                                   "password": "password"})

    assert resp.status_code == 400

def test_invalid_password():
    
    # Too short password
    resp = requests.post(url + "createNewUser",
                             json={
                                 "email": "email@email.com",
                                 "username": "username",
                                 "password": "1234"})

    assert resp.status_code == 400
    
    #Too long password
    resp = requests.post(url + "createNewUser",
                             json={"email": "email@email.com",
                                   "username": "username",
                                   "password": "24321432142341234123412341234123lk4j123l4j1l32jd41kl;3d4j12lk;3d4j12l3d4;kj12l3;d41j2k;l3d4j123lk;d4j"})

    assert resp.status_code == 400

def test_duplicate_email():
    
    resp = requests.post(url + "createNewUser",
                             json={
                                 "email": "email@email.com",
                                 "username": "Username",
                                 "password": "password"})

    assert resp.status_code == 200
    
    resp = requests.post(url + "createNewUser",
                             json={
                                 "email": "email@email.com",
                                 "username": "Username",
                                 "password": "password"})

    assert resp.status_code == 400

def test_working():
    
    resp = requests.post(url + "createNewUser",
                             json={
                                 "email": "email2@email.com",
                                 "username": "Username2",
                                 "password": "password"})

    assert resp.status_code == 200
    
    assert json.loads(resp.text) == {"success" : True}

'''
            ========================================================
                            session tests
            ========================================================
'''

def test_invalid_login():
    # Invalid email
    resp = requests.post(url + "newSession", json = {'username' : "dfasfasdfas", 'password' : "dfasdfasfas"})
    
    assert resp.status_code == 400
    
    resp = requests.post(url + "createNewUser",
                             json={
                                 "email": "email3@email.com",
                                 "username": "Username3",
                                 "password": "password"})

    resp = requests.post(url + "newSession", json = {'username' : "Username3", 'password' : "dfasdfasfas"})
    
    assert resp.status_code == 400

def test_invalid_token():
    resp = requests.post(url + "endSession", json = {'token' : "invalid_token"})
    assert resp.status_code == 403

def test_working_session():
    requests.post(url + "createNewUser",
                             json={
                                 "email": "email4@email.com",
                                 "username": "Username4",
                                 "password": "password"})
    
    resp = requests.post(url + "newSession", json = {'username' : "Username4", 'password' : "password"})
    
    assert resp.status_code == 200
    
    token = json.loads(resp.text)['token']
    
    resp = requests.post(url + "endSession", json = {'token' : token})
    
    assert resp.status_code == 200
    
    resp = requests.post(url + "endSession", json = {'token' : token})
    
    assert resp.status_code == 400