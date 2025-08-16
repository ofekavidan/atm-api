from decimal import Decimal, getcontext, ROUND_HALF_UP
from threading import Lock
from typing import Dict

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, field_validator

# --- money precision ---
getcontext().prec = 28
getcontext().rounding = ROUND_HALF_UP

app = FastAPI(
    title="ATM API",
    version="1.0.0",
    description="Simple in-memory ATM service: balance, deposit, withdraw."
)

# ----- request/response -----

class AmountIn(BaseModel):
    amount: Decimal

    @field_validator("amount")
    @classmethod
    def must_be_positive_with_two_decimals(cls, v: Decimal) -> Decimal:
        if v <= 0:
            raise ValueError("amount must be greater than 0")
        if v.quantize(Decimal("0.01")) != v:
            raise ValueError("amount must have at most 2 decimal places")
        return v

class BalanceOut(BaseModel):
    account_number: str
    balance: Decimal

# ----- in-memory store -----

class Account:
    def __init__(self, balance: Decimal):
        self.balance: Decimal = balance
        self.lock = Lock()

ACCOUNTS: Dict[str, Account] = {
    "1001": Account(Decimal("500.00")),
    "2002": Account(Decimal("1250.50")),
}

def get_account_or_404(account_number: str) -> Account:
    acc = ACCOUNTS.get(account_number)
    if acc is None:
        raise HTTPException(status_code=404, detail="Account not found")
    return acc

# ----- routes -----

@app.get("/accounts/{account_number}/balance", response_model=BalanceOut)
def get_balance(account_number: str):
    acc = get_account_or_404(account_number)
    with acc.lock:
        return BalanceOut(account_number=account_number, balance=acc.balance)

@app.post("/accounts/{account_number}/deposit", response_model=BalanceOut)
def deposit(account_number: str, body: AmountIn):
    acc = get_account_or_404(account_number)
    with acc.lock:
        acc.balance = (acc.balance + body.amount).quantize(Decimal("0.01"))
        return BalanceOut(account_number=account_number, balance=acc.balance)

@app.post("/accounts/{account_number}/withdraw", response_model=BalanceOut)
def withdraw(account_number: str, body: AmountIn):
    acc = get_account_or_404(account_number)
    with acc.lock:
        if body.amount > acc.balance:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        acc.balance = (acc.balance - body.amount).quantize(Decimal("0.01"))
        return BalanceOut(account_number=account_number, balance=acc.balance)

@app.get("/health")
def health():
    return {"status": "ok"}
