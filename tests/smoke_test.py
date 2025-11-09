import sys, os
sys.path.append(os.path.abspath("."))
from fastapi.testclient import TestClient
from app.main import api

client = TestClient(api)

def test_missing_name():
    r = client.post("/chat", json={"user_name": None, "user_message": "hi"})
    assert r.status_code == 200
    assert "name" in r.json()["answer"].lower()
    assert r.json()["patient_found"] is False


def test_known_patient():
    r = client.post("/chat", json={"user_name": "Ravi Kumar", "user_message": "hello"})
    assert r.status_code == 200
    assert "ravi kumar" in r.json()["answer"].lower()
    assert r.json()["patient_found"] is True


def test_clinical_query():
    r = client.post("/chat", json={"user_name": "Ravi Kumar", "user_message": "I have leg swelling"})
    assert r.status_code == 200
    assert r.json()["from_source"] in (None, "reference", "web")
