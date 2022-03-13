

from app.models import db, Call


def log_health_check():
    new_call = Call(APICall = "health_check", userAuth = False)
    
    db.session.add(new_call)
    db.session.commit()