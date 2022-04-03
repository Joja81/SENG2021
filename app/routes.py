from datetime import datetime
import json
from app.functions import healthCheck, emailSystem, authentication, commReport, log
from flask import current_app as app, request
import time
from app.models import Session, db



@app.before_request
def delete_old_sessions():
    sessions = Session.query.filter(Session.time < time.time() - authentication.SESSION_LENGTH*60).all()

    for curr in sessions:
        db.session.delete(curr)
    db.session.commit()

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("working")

@app.route("/invoice/extract_and_send/v1", methods = ["POST"])
@app.route("/sendInvoice", methods = ["POST"])                  #deprecated route
def sendInvoiceEmail():
    #Check authentication
    token = request.headers.get('token')
    user_id = authentication.check_token(token)
    XML = request.files.get('file')
    print("XML OUTPUT")
    if XML == None:
        comm_Report = commReport.communication_report([1], datetime.now())
    else:
        xml = XML.read()
        comm_Report, email_address = emailSystem.send_email(xml, datetime.now())
        log.log_send_invoice(user_id, email_address)

    return comm_Report

@app.route("/invoice/extract_and_send/v2", methods = ["POST"])
def send_invoice_string_Email():
    #Check authentication
    token = request.headers.get('token')
    user_id = authentication.check_token(token)
    data = request.get_json()
    print(data)
    XML = data["file"]
    if XML == None:
        comm_Report = commReport.communication_report([1], datetime.now())
    else:
        comm_Report, email_address = emailSystem.send_email(XML, datetime.now())
        log.log_send_invoice(user_id, email_address)

    return comm_Report

@app.route("/invoice/send_to_email/v1", methods = ["POST"])
@app.route("/emailInvoice", methods = ["POST"])                 #deprecated route
def emailInvoice():
    token = request.headers.get('token')
    email = request.headers.get('email')
    user_id = authentication.check_token(token)

    XML = request.files.get('file')
    xml = XML.read()
    commReport, email_address = emailSystem.send_to_email(xml, email, datetime.now())

    log.log_send_invoice(user_id, email_address)

    return commReport

@app.route("/create/newuser", methods = ["POST"])
@app.route("/createNewUser", methods = ["POST"])                #deprecated route
def createNewUser():
    data = request.get_json()

    response, user_id = authentication.create_user(data)

    log.log_authentication(user_id, call_type="createNewUser")

    return json.dumps(response)

@app.route("/session/start", methods = ["POST"])
@app.route("/newSession", methods = ["POST"])                   #deprecated route
def newSession():

    data = request.get_json()

    response, user_id = authentication.create_session(data['username'], data['password'])

    log.log_authentication(user_id, call_type="newSession")

    return json.dumps(response)

@app.route("/session/end", methods = ['POST'])
@app.route("/endSession", methods = ['POST'])                   #deprecated route
def endSession():
    data = request.get_json()

    response, user_id = authentication.remove_session(data['token'])

    log.log_authentication(user_id, call_type="endSession")

    return json.dumps(response)

@app.route("/health/check/v1", methods = ["GET"])
@app.route("/healthCheck", methods = ["GET"])                   #deprecated route
def getHealthCheck():
    healthInfo = healthCheck.healthCheckInfo()
    log.log_health_check()
    return json.dumps(healthInfo)