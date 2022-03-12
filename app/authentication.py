import os
from pydoc import describe

from sqlalchemy import desc
from app.email import validate_email
from app.error import AccessError, InputError
from app.models import Session, User, db

import jwt

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
    validate_email(request['email'])
    
    # Check valid username
    if len(request['username']) > 100 or len(request['username']) < 5:
        raise InputError(description="Username is invalid. Must be 5-100 characters long")
    
    # Check password valid
    if len(request['password']) > 100 or len(request['password']) < 5:
        raise InputError(description="Password is invalid. Must be 5-100 characters long")
    
    # Check for duplicate email
    if User.query.filter(User.email == request['email']).count() != 0:
        raise InputError(description="Email is already in use")
    
    # Check username for duplicate
    if User.query.filter(User.username == request['username']).count() != 0:
        raise InputError(description="Username is already in use")
    
    #Create new user
    new_user = User(email = request['email'], username = request['username'], password = request['password'])
    
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
    
    user = User.query.filter(User.username == username, User.password == password).first()
    
    if user is None:
        raise InputError(description="Login details are invalid")
    
    new_session = Session(user = user)
    
    db.session.add(new_session)
    db.session.commit()
    
    token = jwt.encode({'username' : user.username, 'session_id' : new_session.id}, SECRET,  algorithm='HS256')
    
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
    
    try:
        data = jwt.decode(token, SECRET, algorithms=['HS256'])
    except BaseException as all_errors:
        raise AccessError(description= "Token is not valid") from all_errors
    
    session = Session.query.get(data['session_id'])
    
    if session == None:
        raise InputError(description="Session does not exist")
    
    db.session.delete(session)
    db.session.commit()
    
    return {}