from __init__ import startTime
from datetime import datetime

def healthCheckInfo():
    upTime = datetime.now() - startTime
    alive = True
    return {'alive': alive, 'serverUpTime': upTime}