from app import startTime
from datetime import datetime

from app.models import Call

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
    startTimeUnix = datetime.timestamp(startTime)
    currTimeUnix = datetime.timestamp(datetime.now())
    upTime = currTimeUnix - startTimeUnix
    alive = True
    
    call_num = Call.query.filter(Call.timeCalled > startTimeUnix).count()
    
    return {'alive': alive, 'serverUpTime': upTime, 'numTransactions' : call_num, 'currentVersion' : "Version 1 release"}