from app.email import validate_email
from app.error import InputError
from app.models import User, db


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