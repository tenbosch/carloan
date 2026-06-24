from flask import Flask, render_template, request, jsonify
from datetime import date
import calendar

app = Flask(__name__)

LOAN_TERMS = {
    24: 3.74,
    36: 3.99,
    48: 4.24,
    60: 4.49,
    72: 4.74,
    84: 4.99,
}


def add_months(dt, months):
    month = dt.month - 1 + months
    year = dt.year + month // 12
    month = month % 12 + 1
    day = min(dt.day, calendar.monthrange(year, month)[1])
    return date(year, month, day)


def calculate_loan(car_cost, tax_rate, dealer_fees, down_payment, annual_rate, term_months, start_date, extra_monthly=0):
    loan_amount = (car_cost * (1 + tax_rate / 100)) + dealer_fees - down_payment

    if loan_amount <= 0:
        return {'error': 'Down payment exceeds the financed amount.'}

    r = annual_rate / 100 / 12
    n = term_months

    if r == 0:
        monthly_payment = loan_amount / n
    else:
        monthly_payment = loan_amount * (r * (1 + r) ** n) / ((1 + r) ** n - 1)

    schedule = []
    balance = loan_amount
    total_interest = 0

    for i in range(1, n + 1):
        if balance <= 0.005:
            break

        payment_date = add_months(start_date, i)
        interest = balance * r
        principal = monthly_payment - interest

        if principal + extra_monthly >= balance:
            # Final payment — pay off remaining balance
            principal = balance
            extra = 0.0
            actual_payment = principal + interest
        else:
            extra = extra_monthly
            actual_payment = monthly_payment

        balance -= (principal + extra)
        total_interest += interest

        schedule.append({
            'num': i,
            'date': payment_date.strftime('%Y-%m-%d'),
            'payment': round(actual_payment, 2),
            'principal': round(principal, 2),
            'interest': round(interest, 2),
            'extra': round(extra, 2),
            'balance': round(max(balance, 0), 2),
        })

        if balance <= 0.005:
            break

    return {
        'loan_amount': round(loan_amount, 2),
        'monthly_payment': round(monthly_payment, 2),
        'total_interest': round(total_interest, 2),
        'total_cost': round(loan_amount + total_interest, 2),
        'payoff_months': len(schedule),
        'schedule': schedule,
    }


@app.route('/')
def index():
    return render_template('index.html', loan_terms=LOAN_TERMS)


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    try:
        car_cost = float(data['car_cost'])
        tax_rate = float(data['tax_rate'])
        dealer_fees = float(data['dealer_fees'])
        down_payment = float(data['down_payment'])
        annual_rate = float(data['annual_rate'])
        term_months = int(data['term_months'])
        start_date = date.fromisoformat(data['start_date'])
        extra_monthly = float(data.get('extra_monthly', 0))
    except (KeyError, ValueError, TypeError) as e:
        return jsonify({'error': f'Invalid input: {e}'}), 400

    result = calculate_loan(
        car_cost, tax_rate, dealer_fees, down_payment,
        annual_rate, term_months, start_date, extra_monthly
    )

    if 'error' in result:
        return jsonify(result), 400

    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
