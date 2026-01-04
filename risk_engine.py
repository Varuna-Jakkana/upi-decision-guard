from datetime import datetime

def is_late_night(time_str):
    """Check if payment time is late night (23:00-06:00)"""
    t = datetime.strptime(time_str, "%H:%M").time()
    return t.hour >= 23 or t.hour < 6

def calculate_risk(amount, category, time_str, todays_category_count, category_used, category_limit):
    """Calculate risk level based on 3 factors"""
    # 1. Time risk (late night)
    time_risk = 1 if is_late_night(time_str) else 0
    
    # 2. Frequency risk (too many same category today)
    freq_risk = 1 if todays_category_count >= 3 else 0
    
    # 3. Budget risk (70%+ used)
    budget_ratio = category_used / category_limit if category_limit > 0 else 0
    budget_risk = 1 if budget_ratio >= 0.7 else 0
    
    # Score 0-1
    score = (time_risk + freq_risk + budget_risk) / 3
    
    if score >= 0.66:
        level = "high"
        msg = "🚨 HIGH RISK: Late night + frequent spending + near budget limit!"
    elif score >= 0.33:
        level = "medium" 
        msg = "⚠️ MEDIUM: Close to category limit."
    else:
        level = "low"
        msg = "✅ LOW: This payment looks safe."
    
    return level, msg
