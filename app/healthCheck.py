from __init__ import startTime
from datetime import datetime

def healthCheckInfo():
    '''
    Returns information about the current state of the server, such as if the 
    server is alive and how long the server has been running

    Arguments:
        None

    Exceptions:
        InputError  - None
        AccessError - None

    Return Value:
        Returns {'alive': alive, 'serverUpTime': upTime}
    '''

    upTime = datetime.now() - startTime
    alive = True
    return {'alive': alive, 'serverUpTime': upTime}