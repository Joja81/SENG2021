from crypt import methods
import json
from app.functions import ublExtractor, healthCheck
from flask import current_app as app, request
from app.functions import emailSystem
from app.functions.authentication import check_token, create_session, create_user, remove_session

from app.models import db, User, Call

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("Working")

@app.route("/sendInvoice", methods = ["POST"])
def sendInvoiceEmail():
    #Check authentication
    token = request.headers.get('token')
    check_token(token)
    
    XML = request.files.get('file')
    xml = XML.read()
    
    emailSystem.send_email(xml)
    return json.dumps("Communication report") #waiting for communication report implementation

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
    return json.dumps(healthInfo)

