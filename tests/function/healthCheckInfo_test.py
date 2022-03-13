import pytest
from app import healthCheck
from datetime import datetime

def test_health_check_info():
    info = healthCheck.healthCheckInfo()
    assert info['alive'] == True
    assert info['serverUpTime'] > 0