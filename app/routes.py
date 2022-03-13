from datetime import datetime
import json
from app import ublExtractor, healthCheck
from flask import current_app as app, request
from app import email

from app.models import db, User, Call

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("Working")

@app.route("/sendinvoice", methods = ["POST"])
def sendInvoiceEmail():
    XML = request.files.get('file')
    xml = XML.read() 
    commReport = email.send_email(xml, datetime.now())
    return json.dumps(commReport)

@app.route("/HealthCheck", methods = ["GET"])
def getHealthCheck():
    healthInfo = healthCheck.healthCheckInfo()
    return json.dumps(healthInfo)

