import pytest
from app import healthCheck
from datetime import datetime

def test_health_check_info():
    info = healthCheck.healthCheckInfo()
    testTime = datetime.now() - datetime.now()
    assert info['alive'] == True
    assert info['serverUpTime'] > testTime