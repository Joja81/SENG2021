from crypt import methods
import json
from flask import current_app as app, request

@app.route("/", methods = ["GET"])
def test():
    return json.dumps("Working")