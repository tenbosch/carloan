# Car Loan Calculator

A single-page Flask app that computes car loan amortization schedules and models the impact of extra monthly principal payments.

## Features

- Calculates loan amount from car cost, sales tax, dealer fees, and down payment
- Auto-fills interest rate based on selected loan term (24–84 months)
- Full month-by-month amortization schedule with payment dates
- Extra principal payment tool — shows months saved and interest avoided vs. the baseline

## Setup

```bash
python -m venv .venv
source .venv/Scripts/activate   # Windows (Git Bash / MSYS2)
# or: .venv\Scripts\activate    # Windows (cmd / PowerShell)
# or: source .venv/bin/activate # macOS / Linux
pip install -r requirements.txt
python app.py
```

Open http://127.0.0.1:5000 in your browser.

## Usage

1. Enter car cost, sales tax rate, dealer fees, and down payment.
2. Select a loan term — the interest rate auto-fills with a default APR.
3. Override the interest rate if your lender's rate differs.
4. Click **Calculate** to see the summary and full amortization table.
5. Enter an extra monthly principal amount and click **Recalculate** to see how much sooner the loan pays off and how much interest you save.

## Loan Formula

```
loan_amount  = (car_cost × (1 + tax_rate/100)) + dealer_fees − down_payment
monthly_rate = annual_rate / 100 / 12
payment      = loan_amount × r(1+r)^n / ((1+r)^n − 1)
```

## Stack

- **Backend:** Python 3, Flask — single `app.py` file, no database
- **Frontend:** Vanilla JS + Jinja2 template, no build step required
