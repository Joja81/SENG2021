import json
from flask import current_app as app, request
from app import email
from app.authentication import create_user

from app.models import db, User, Call

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("Working")

@app.route("/sendinvoice", methods = ["POST"])
def sendInvoiceEmail():
    XML = request.files.get('file')
    xml = XML.read()
    email.send_email(xml)
    return json.dumps("Communication report") #waiting for communication report implementation

@app.route("/createNewUser", methods = ["POST"])
def createNewUser():
    data = request.get_json()
    return json.dumps(create_user(data))