# tests/test_alerting.py
def test_phishing_alert():
    test_event = {
        "type": "phishing_detection",
        "severity": 5,
        "message": "CEO Fraud Attempt"
    }
    kafka.produce('shieldnet-alerts', json.dumps(test_event))
    assert check_elastic_alert_exists("CEO Fraud")
