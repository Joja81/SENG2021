

from app.models import db, Call


def log_health_check():
    new_call = Call(APICall = "health_check", userAuth = False)
    
    db.session.add(new_call)
    db.session.commit()
    
def log_send_invoice(user_id, email_adress):
    
    print(email_adress)
    print(user_id)
    
    new_call = Call(APICall = "send_invoice", userId = user_id,  userTo = email_adress, userAuth = True)
    db.session.add(new_call)
    db.session.commit()