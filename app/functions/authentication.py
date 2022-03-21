import hashlib
import os
from pydoc import describe

from sqlalchemy import desc
from app.functions.emailSystem import validate_email
from app.functions.error import AccessError, InputError
from app.models import Session, User, db
import time

import jwt

SESSION_LENGTH = 60 # Number of minutes session should exist for

SECRET = os.environ.get('SECRET')

def create_user(request):
    """
    Creates user and adds them to the database.

    Raises issue if variables given are invalid:
        - Invalid/duplicate email
        - Invalid username or password (Must be 5-100 char long)
        - Duplicate username

    Parameters
    ----------
    {
        'email' : (String)
        'username' : (String)
        'password' : (String)
    }

    Returns
    -------
    {
        'success' : (Boolean)
    }
    """

    # Check for valid email
    if not validate_email(request['email']):
        raise InputError("Email is not valid")
    
    # Check valid username
    if len(request['username']) > 100 or len(request['username']) < 5:
        raise InputError(description="Username is invalid. Must be 5-100 characters long")
    
    # Check password valid
    if len(request['password']) > 100 or len(request['password']) < 5:
        raise InputError(description="Password is invalid. Must be 5-100 characters long")
    
    password = hash(request['password'])
    
    # Check for duplicate email
    if User.query.filter(User.email == request['email']).count() != 0:
        raise InputError(description="Email is already in use")
    
    # Check username for duplicate
    if User.query.filter(User.username == request['username']).count() != 0:
        raise InputError(description="Username is already in use")
    
    #Create new user
    new_user = User(email = request['email'], username = request['username'], password = password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return {'success' : True}

def create_session(username, password):
    """
    Checks user login credentials and creates a session for them if valid.

    Raises issue if login details are invalid.

    Parameters
    ----------
    username (String)
    password (String)

    Returns
    -------
    {
        'token' : (String)
    }
    """
    
    password = hash(password)
    
    user = User.query.filter(User.username == username, User.password == password).first()
    
    if user is None:
        raise InputError(description="Login details are invalid")
    
    new_session = Session(user = user, time = time.time())
    
    db.session.add(new_session)
    db.session.commit()
    
    print("About to generate token")

    print(f"Username: {user.username}")
    print(f"Session id: {new_session.id}")

    token = jwt.encode({'username' : user.username, 'session_id' : new_session.id}, SECRET,  algorithm='HS256')
    
    print("Token start")
    print(token)
    print("Token end")

    return {'token' : token}

def remove_session(token):
    """
    Ends session if the token is valid.

    Raises issue if invalid token.

    Parameters
    ----------
    token (String)

    Returns
    -------
    {}
    """
    session = load_token(token)
    
    db.session.delete(session)
    db.session.commit()
    
    return {}

def check_token(token):
    """
    Checks if token is valid and returns user id if it is.

    Parameters
    ----------
    token (String)

    Returns
    -------
    user_id
    """
    
    session = load_token(token)
    
    return session.userId

def load_token(token):
    """
    Loads token. Throws error is token is invalid.

    Parameters
    ----------
    token (String)

    Returns
    -------
    session (Session)
    """
    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
    except BaseException as all_errors:
        raise AccessError(description= "Token is not valid") from all_errors
    
    session = Session.query.get(data['session_id'])
    
    if session == None:
        raise InputError(description="Session does not exist")
    return session

def hash(input):
    '''
    Generates hash using sha256 and returns as string
    '''

    return hashlib.sha256(input.encode()).hexdigest()