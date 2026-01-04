from datetime import datetime

def calculate_risk(amount, category, time_str, todays_category_count,
                   category_used, category_limit, transactions=None, user_config=None):
    risks = []
    
    # Safe defaults
    if user_config is None:
        user_config = {"budget": 8000}
    if transactions is None:
        transactions = []
    
    # Get current month for filtering
    current_month = datetime.now().strftime("%Y-%m")
    
    # Late night spending
    try:
        t = datetime.strptime(time_str, "%H:%M").time()
        if t.hour >= 22 or t.hour <= 2:
            risks.append("Late night purchase detected")
            risks.append("Unusual spending hour detected")
    except:
        pass
    
    # High amount
    if amount > 500:
        risks.append("High transaction amount")
    
    # Category overuse
    if category_used + amount > category_limit * 0.8:
        risks.append(f"{category} budget almost exhausted")
    
    # GENIUS: Tiered monthly alerts + category validation (REPLACE HERE)
    category_total_limit = sum(user_config["category_limits"].values())
    if category_total_limit > user_config["budget"] * 1.2:
        risks.append("⚠️ Category limits exceed monthly budget")
    
    monthly_spent = sum(t["amount"] for t in transactions)
    if monthly_spent + amount > user_config["budget"] * 0.9:
        risks.append("🚨 SEVERE: 90%+ MONTHLY BUDGET EXHAUSTED!")
        risks.append("STOP SPENDING IMMEDIATELY!")
    elif monthly_spent + amount > user_config["budget"] * 0.5:
        risks.append("⚠️ WARNING: 50%+ Monthly budget used")
    
    # Frequent category use
    if todays_category_count >= 3:
        risks.append("Frequent spending in same category")
    
    risk_count = len(risks)
    if risk_count >= 3:
        return "high", "🚨 HIGH RISK - Multiple red flags! Strongly recommend canceling."
    elif risk_count >= 2:
        return "medium", "⚠️ MEDIUM RISK - Proceed with caution."
    else:
        return "low", "✅ LOW RISK - Safe to proceed."
