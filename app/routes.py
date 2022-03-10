from crypt import methods
import json
from app import ublExtractor, healthCheck
from flask import current_app as app, request

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("Working")

@app.route("/sendinvoice/email", methods = ["POST"])
def sendInvoiceEmail():
    XML = request.files.get('file')
    xml = XML.read()
    contacts = ublExtractor.customerContact(xml)
    #email(contacts) waiting for send email implementation
    return json.dumps("Communication report") #waiting for communication report implementation

@app.route("/HealthCheck", methods = ["GET"])
def getHealthCheck():
    healthInfo = healthCheck.healthCheckInfo()
    return dumps(healthInfo)

