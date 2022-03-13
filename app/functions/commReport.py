from datetime import datetime
import json

# dictionary of error code messages, can update as we need
error_messages = {
    1: 'XML not found. ',
    2: 'Invoice file size over 10MB. ',
    3: 'Email is not of valid format. ',
    4: 'Server not connected. ',
    5: 'Server rejected all recipients (mail not sent). '
    }

"""
    Returns a communication report in JSON form, with status, time sent
    and errors in readable format.

    Parameters
        error_codes : list
            A list of error codes (int).
        time_sent : datetime
            Datetime of time email was sent.
        connected : bool
            If server is connected.

    Returns
        JSON communication report.

    """
def communication_report(error_codes: list, time_sent: datetime):
    report_dict = {
        "sentMail": error_codes == [],  
        "readable_errors": '',
        "xmlFound": 1 not in error_codes,
        "xmlRightSize": (1 and 2) not in error_codes,
        "emailValid": 3 not in error_codes,
        "connectedToMail": 4 not in error_codes,
        "timeSent": time_sent.strftime("%m/%d/%Y, %H:%M:%S"),
        "timeTaken": (datetime.now() - time_sent).total_seconds()
    }
    for error_code in error_codes:
        if error_messages.get(error_code):
            report_dict['readable_errors'] += (error_messages.get(error_code))
    return json.dumps(report_dict)