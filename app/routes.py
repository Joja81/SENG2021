from datetime import datetime
import json
from app.functions import ublExtractor, healthCheck
from flask import current_app as app, request
from app.functions import emailSystem
from app.functions.authentication import SESSION_LENGTH, check_token, create_session, create_user, remove_session
from app.functions.log import log_health_check, log_send_invoice
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
    xml = XML.read() 
    commReport, email_address = emailSystem.send_email(xml, datetime.now())
    
    log_send_invoice(user_id, email_address)
    
    return commReport

@app.route("/createNewUser", methods = ["POST"])
def createNewUser():
    data = request.get_json()
    return json.dumps(create_user(data))

@app.route("/newSession", methods = ["POST"])
def newSession():
    
    data = request.get_json()
    
    return json.dumps(create_session(data['username'], data['password']))

@app.route("/endSession", methods = ['POST'])
def endSession():
    data = request.get_json()
    
    return json.dumps(remove_session(data['token']))
@app.route("/healthCheck", methods = ["GET"])
def getHealthCheck():
    healthInfo = healthCheck.healthCheckInfo()
    log_health_check()
    return json.dumps(healthInfo)