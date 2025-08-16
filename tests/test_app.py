from fastapi.testclient import TestClient
from app import app, ACCOUNTS
from decimal import Decimal

client = TestClient(app)

def test_get_balance_ok():
    r = client.get("/accounts/1001/balance")
    assert r.status_code == 200
    data = r.json()
    assert data["account_number"] == "1001"
    assert "balance" in data

def test_deposit_and_withdraw_flow():
    start = ACCOUNTS["1001"].balance
    r1 = client.post("/accounts/1001/deposit", json={"amount": "10.00"})
    assert r1.status_code == 200
    r2 = client.post("/accounts/1001/withdraw", json={"amount": "5.00"})
    assert r2.status_code == 200
    after = Decimal(r2.json()["balance"])
    assert after == (start + Decimal("5.00")).quantize(Decimal("0.01"))

def test_withdraw_insufficient_funds():
    r = client.post("/accounts/1001/withdraw", json={"amount": "999999.99"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Insufficient funds"
