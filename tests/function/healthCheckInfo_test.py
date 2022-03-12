import pytest
from app import healthCheck

def test_health_check_info():
    info = healthCheck.healthCheckInfo()
    assert info['alive'] == True
    assert info['serverUpTime'] > 0