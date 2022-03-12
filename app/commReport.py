from datetime import datetime
import json

# dictionary of error code messages, can update as we need
error_messages = {
    1:'Email is not of valid format. ',
    2:'Invoice file size over 10MB. ',
    3:'Server not connected. '
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
def communication_report(error_codes: list, time_sent: datetime, connected: bool):
    report_dict = {
        "readable_message": '',
        "xmlFound": True,
        "xmlRightSize": False if (2 in error_codes) else True,
        "emailValid": False if (1 in error_codes) else True,
        "connectedToMail": connected,
        "sentMail": error_codes == [],
        "timeSent": time_sent.strftime("%m/%d/%Y, %H:%M:%S"),
        "timeTaken": (datetime.now() - time_sent).total_seconds()
    }
    for error_code in error_codes:
        if error_messages.get(error_code):
            report_dict['errors'].append(error_messages.get(error_code))
    return json.dumps(report_dict)