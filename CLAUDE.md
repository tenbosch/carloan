# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the app

```bash
source .venv/Scripts/activate   # Windows Git Bash / activate venv
python app.py                    # starts Flask dev server on http://127.0.0.1:5000
```

To set up from scratch:
```bash
python -m venv .venv
source .venv/Scripts/activate
pip install -r requirements.txt
python app.py
```

## Architecture

Single-file Flask app with one Jinja2 template. No database — all calculations are stateless.

**`app.py`** contains everything backend:
- `LOAN_TERMS` dict maps term (months) → default APR; passed to the template so the JS dropdown can auto-fill rates.
- `calculate_loan()` is the core function — computes loan principal, standard amortization payment, then walks the schedule month-by-month. Extra monthly principal shortens the schedule early by consuming balance faster.
- `add_months()` handles end-of-month edge cases without `python-dateutil`.
- `POST /calculate` is the only API endpoint; the frontend calls it via `fetch` and renders the results entirely client-side.

**`templates/index.html`** is a single-page app in a Jinja2 template:
- On load, `LOAN_TERMS` is injected via `{{ loan_terms | tojson }}` so the JS can auto-fill the interest rate when the term dropdown changes.
- `calculate()` calls `POST /calculate` with `extra_monthly=0` and stores the result in `baseResult`.
- `applyExtra()` re-calls the same endpoint with the extra payment amount and diffs against `baseResult` to render the savings banner.
- All currency formatting is done client-side with `toLocaleString('en-US')`.

## Loan formula reference

```
loan_amount  = (car_cost × (1 + tax_rate/100)) + dealer_fees − down_payment
monthly_rate = annual_rate / 100 / 12
payment      = loan_amount × r(1+r)^n / ((1+r)^n − 1)
```
