from datetime import datetime
import json

# dictionary of error code messages, can update as we need
error_messages = {
    1:'Invalid email address. ',
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

    Returns
        JSON communication report.

    """
def communication_report(error_codes: list, time_sent: datetime):
    report_dict = {
        'status': 'Success' if error_codes == [] else 'Failed',
        'time_sent': time_sent.strftime("%m/%d/%Y, %H:%M:%S"),
        'errors': ''
    }
    for error_code in error_codes:
        if error_messages.get(error_code):
            report_dict['errors'].append(error_messages.get(error_code))
    return json.dumps(report_dict)