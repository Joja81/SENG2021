

import time
from app.models import db, Call


def log_health_check():
    """
    Logs health_check call
    
    Parameters
    None

    Returns
    None
    """
    
    new_call = Call(APICall = "health_check", userAuth = False, timeCalled = time.time())
    
    db.session.add(new_call)
    db.session.commit()
    
def log_send_invoice(user_id, email_adress):
    """
    Logs send_invoice call and saves details about transaction.
    
    Parameters
    user_id (Integer)
    email_adress (String)

    Returns
    None
    """
    
    new_call = Call(APICall = "send_invoice", userId = user_id,  userTo = email_adress, userAuth = True, timeCalled = time.time())
    
    db.session.add(new_call)
    db.session.commit()


def log_authentication(user_id, call_type):
    """
    Logs authentication call and saves details about transaction
    
    Parameters
    user_id (Integer)
    call_type (String)

    Returns
    None
    """

    new_call = Call(APICall = call_type, userId = user_id, userAuth = True, timeCalled = time.time())
    
    db.session.add(new_call)
    db.session.commit()