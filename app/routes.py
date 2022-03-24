from datetime import datetime
import json
from app.functions import ublExtractor, healthCheck
from flask import current_app as app, request
from app.functions import emailSystem
from app.functions.authentication import SESSION_LENGTH, check_token, create_session, create_user, remove_session
from app.functions.commReport import communication_report
from app.functions.log import log_authentication, log_health_check, log_send_invoice
import time

from app.models import Session, db, User, Call



@app.before_request
def delete_old_sessions():
    sessions = Session.query.filter(Session.time < time.time() - SESSION_LENGTH*60).all()
    
    for curr in sessions:
        db.session.delete(curr)
    db.session.commit()

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("working")

@app.route("/sendInvoice", methods = ["POST"])
def sendInvoiceEmail():
    #Check authentication
    token = request.headers.get('token')
    user_id = check_token(token)
    XML = request.files.get('file')
    print("XML OUTPUT")
    if XML == None:
        commReport = communication_report([1], datetime.now())
    else:
        xml = XML.read()
        commReport, email_address = emailSystem.send_email(xml, datetime.now())
    
        log_send_invoice(user_id, email_address)
    
    return commReport

@app.route("/emailInvoice", methods = ["POST"])
def emailInvoice():
    token = request.headers.get('token')
    email = request.headers.get('email')
    user_id = check_token(token)
    
    XML = request.files.get('file')
    xml = XML.read() 
    commReport, email_address = emailSystem.send_to_email(xml, email, datetime.now())
    
    log_send_invoice(user_id, email_address)
    
    return commReport

@app.route("/createNewUser", methods = ["POST"])
def createNewUser():
    data = request.get_json()

    response, user_id = create_user(data)

    log_authentication(user_id, call_type="createNewUser")

    return json.dumps(response)

@app.route("/newSession", methods = ["POST"])
def newSession():
    
    data = request.get_json()

    response, user_id = create_session(data['username'], data['password'])

    log_authentication(user_id, call_type="newSession")
    
    return json.dumps(response)

@app.route("/endSession", methods = ['POST'])
def endSession():
    data = request.get_json()
    
    response, user_id = remove_session(data['token'])

    log_authentication(user_id, call_type="endSession")

    return json.dumps(response)
    
    return json.dumps(remove_session(data['token']))
@app.route("/healthCheck", methods = ["GET"])
def getHealthCheck():
    healthInfo = healthCheck.healthCheckInfo()
    log_health_check()
    return json.dumps(healthInfo)