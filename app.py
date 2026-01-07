from flask import Flask, render_template, request, redirect, url_for, flash, session
app = Flask(__name__)
app.secret_key = 'upi-guard-2026-secret'


transactions = []
user_config = {
    "budget": 10000, 
    "total_spent": 0, 
    "remaining": 10000, 
    "budgets": {
        "Food": {"limit": 0, "spent": 0},
        "Shopping": {"limit": 0, "spent": 0},
        "Entertainment": {"limit": 0, "spent": 0},
        "Bills": {"limit": 0, "spent": 0},
        "Health": {"limit": 0, "spent": 0},
        "Savings": {"limit": 0, "spent": 0},
        "Others": {"limit": 0, "spent": 0}
    }
}


# Load saved config
try:
    with open('config.txt', 'r') as f:
        lines = f.readlines()
        for line in lines:
            key, val = line.strip().split('=')
            if key == 'budget':
                user_config['budget'] = float(val)
                user_config['remaining'] = float(val)
            elif key in ['food', 'shopping', 'entertainment', 'bills', 'health', 'savings', 'others']:
                category_map = {
                    'food': 'Food',
                    'shopping': 'Shopping',
                    'entertainment': 'Entertainment',
                    'bills': 'Bills',
                    'health': 'Health',
                    'savings': 'Savings',
                    'others': 'Others'
                }
                user_config['budgets'][category_map[key]]['limit'] = float(val)
except:
    pass  # First run


@app.route('/')
def home():
    return redirect(url_for('setup'))


@app.route('/setup', methods=['GET', 'POST'])
def setup():
    if request.method == 'POST':
        try:
            budget = float(request.form['budget'])
            food = float(request.form['food_limit'])
            shopping = float(request.form['shopping_limit'])
            entertainment = float(request.form['entertainment_limit'])
            bills = float(request.form['bills_limit'])
            health = float(request.form['health_limit'])
            savings = float(request.form['savings_limit'])
            others = float(request.form['others_limit'])
            
            total_sum = food + shopping + entertainment + bills + health + savings + others
            
            if abs(budget - total_sum) < 0.01:
                user_config.update({
                    "budget": budget, 
                    "total_spent": 0, 
                    "remaining": budget,
                    "budgets": {
                        "Food": {"limit": food, "spent": 0},
                        "Shopping": {"limit": shopping, "spent": 0},
                        "Entertainment": {"limit": entertainment, "spent": 0},
                        "Bills": {"limit": bills, "spent": 0},
                        "Health": {"limit": health, "spent": 0},
                        "Savings": {"limit": savings, "spent": 0},
                        "Others": {"limit": others, "spent": 0}
                    }
                })
                with open('config.txt', 'w') as f:
                    f.write(f"budget={budget}\nfood={food}\nshopping={shopping}\nentertainment={entertainment}\nbills={bills}\nhealth={health}\nsavings={savings}\nothers={others}\n")
                flash('✅ Budget saved successfully!', 'success')
                return redirect(url_for('dashboard'))
            else:
                flash(f'🚫 Sum ₹{total_sum:.0f} ≠ Budget ₹{budget:.0f}!', 'error')
        except ValueError:
            flash('❌ Invalid numbers entered!', 'error')
    return render_template('setup.html')


@app.route('/dashboard')
def dashboard():
    budget = user_config.get('budget', 10000)
    total_spent = user_config.get('total_spent', 0)
    remaining = user_config.get('remaining', budget)

    return render_template(
        'dashboard.html',
        config=user_config,
        transactions=transactions,
        budget=budget,
        total_spent=total_spent,
        remaining=remaining
    )


@app.route('/add_payment', methods=['GET', 'POST'])
def add_payment():
    if request.method == 'POST':
        return redirect('/confirm_payment')
    return render_template('add_payment.html')


@app.route('/confirm_payment', methods=['POST'])
def confirm_payment():
    merchant = request.form.get('merchant', 'Unknown')
    try:
        amount = float(request.form.get('amount', 0))
        category = request.form.get('category', 'Others')
    except ValueError:
        flash('❌ Invalid amount!', 'error')
        return redirect('/add_payment')
    
    # Store payment details in session temporarily (NOT added to transactions yet)
    session['pending_payment'] = {
        'merchant': merchant,
        'amount': amount,
        'category': category
    }
    
    # AI Risk Analysis
    risk_score = 20
    if 'unknown' in merchant.lower() or 'test' in merchant.lower():
        risk_score += 50
    if amount > user_config['budget'] * 0.2:
        risk_score += 30
    if category == 'Entertainment' and amount > 1000:
        risk_score += 25
    risk_score = min(risk_score, 95)
    
    # Determine if blocked
    blocked = risk_score > 70
    
    # Status
    if risk_score > 70:
        status = "🚨 HIGH RISK - Review Carefully!"
        color = "#ef4444"
    elif risk_score > 40:
        status = "⚠️ CAUTION - Medium Risk"
        color = "#f59e0b"
    else:
        status = "✅ APPROVED - Low Risk"
        color = "#10b981"
    
    return render_template('risk_result.html', risk_score=risk_score, status=status, color=color, merchant=merchant, amount=amount, category=category, blocked=blocked)


@app.route('/approve_payment')
def approve_payment():
    """User approved the payment (low/medium risk or forced proceed on high risk)"""
    pending = session.get('pending_payment')
    
    if not pending:
        flash('❌ No pending payment to approve!', 'error')
        return redirect('/dashboard')
    
    merchant = pending['merchant']
    amount = pending['amount']
    category = pending['category']
    
    # NOW add the transaction
    new_tx = {
        'merchant': merchant,
        'amount': amount,
        'category': category,
        'risk': 0,
        'blocked': False
    }
    transactions.append(new_tx)
    
    # Update totals
    user_config['total_spent'] += amount
    user_config['remaining'] -= amount
    if category in user_config['budgets']:
        user_config['budgets'][category]['spent'] += amount
    
    # Clear pending payment
    session.pop('pending_payment', None)
    
    flash('✅ Payment approved and added!', 'success')
    return redirect('/dashboard')


@app.route('/cancel_payment')
def cancel_payment():
    """User canceled the payment"""
    session.pop('pending_payment', None)
    flash('❌ Payment canceled!', 'error')
    return redirect('/dashboard')


# Keeping force_proceed for backward compatibility (redirect to approve)
@app.route('/force_proceed')
def force_proceed():
    return redirect('/approve_payment')


if __name__ == '__main__':
    app.run(debug=True)
