# ATM API (FastAPI, In-Memory)

Simple server-side ATM with three operations: **get balance**, **deposit**, and **withdraw**.  
All data is kept **in memory** and resets on server restart.

---

## Live

- **Base**: https://atm-api-x9nw.onrender.com  
- **Docs (Swagger)**: https://atm-api-x9nw.onrender.com/docs  
- **Health**: https://atm-api-x9nw.onrender.com/health

---

## Endpoints

| Method | Path                                  | Body (JSON)          | 200 Response (example)                         |
|-------:|---------------------------------------|----------------------|-----------------------------------------------|
| GET    | `/accounts/{account_number}/balance`  | –                    | `{"account_number":"1001","balance":"500.00"}` |
| POST   | `/accounts/{account_number}/deposit`  | `{"amount":"50.00"}` | `{"account_number":"1001","balance":"550.00"}` |
| POST   | `/accounts/{account_number}/withdraw` | `{"amount":"30.00"}` | `{"account_number":"1001","balance":"520.00"}` |

> Notes  
> • `amount` must be **greater than 0** (string or number).  
> • Unknown account → **404**; insufficient funds → **400**.

---

## Run locally:

### Create a virtual environment:

python -m venv .venv

### Activate it

Windows:
.\.venv\Scripts\Activate.ps1

Linux/Mac:
source .venv/bin/activate

### Install dependencies
python -m pip install -r requirements.txt

#### Run the server (open http://127.0.0.1:8000/docs)
python -m uvicorn app:app --reload

### Run tests (in another terminal, or stop the server first)
python -m pytest -q



## Example (curl)

```bash
# Health
curl https://atm-api-x9nw.onrender.com/health

# Balance
curl https://atm-api-x9nw.onrender.com/accounts/1001/balance

# Deposit 50.25
curl -X POST https://atm-api-x9nw.onrender.com/accounts/1001/deposit \
  -H "Content-Type: application/json" \
  -d '{"amount":"50.25"}'

# Withdraw 30.00
curl -X POST https://atm-api-x9nw.onrender.com/accounts/1001/withdraw \
  -H "Content-Type: application/json" \
  -d '{"amount":"30.00"}'
---