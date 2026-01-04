from flask import Flask, render_template, request, redirect, url_for
from risk_engine import calculate_risk

app = Flask(__name__)

# In-memory storage (resets on restart)
transactions = []
user_config = {
    "budget": 8000,
    "category_limits": {"Food": 3000, "Travel": 2000, "Entertainment": 1000},
}
decisions_avoided = 0

@app.route("/")
def dashboard():
    total_spent = sum(t["amount"] for t in transactions)
    categories_stats = []
    for name, limit in user_config["category_limits"].items():
        spent = sum(t["amount"] for t in transactions if t["category"] == name)
        categories_stats.append({"name": name, "spent": spent, "limit": limit})
    
    estimated_saved = decisions_avoided * 100  # Demo estimate
    
    stats = {
        "budget": user_config["budget"],
        "total_spent": total_spent,
        "categories": categories_stats,
        "decisions_avoided": decisions_avoided,
        "estimated_saved": estimated_saved,
    }
    return render_template("dashboard.html", stats=stats)

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/setup", methods=["GET"])
def setup():
    return render_template("setup.html")

@app.route("/setup", methods=["POST"])
def save_setup():
    global user_config
    user_config["budget"] = float(request.form["budget"])
    user_config["category_limits"] = {
        "Food": float(request.form["food_limit"]),
        "Travel": float(request.form["travel_limit"]),
        "Entertainment": float(request.form["entertainment_limit"]),
    }
    return redirect(url_for("dashboard"))

@app.route("/add_payment", methods=["GET", "POST"])
def add_payment():
    if request.method == "GET":
        return render_template("add_payment.html")
    
    # POST - calculate risk
    amount = float(request.form["amount"])
    merchant = request.form["merchant"]
    category = request.form["category"]
    time_str = request.form["time"]
    
    # Simple stats (ignore date for demo)
    todays_category_count = sum(1 for t in transactions if t["category"] == category)
    category_used = sum(t["amount"] for t in transactions if t["category"] == category)
    category_limit = user_config["category_limits"][category]
    
    risk_level, message = calculate_risk(
        amount, category, time_str,
        todays_category_count, category_used, category_limit
    )
    
    return render_template(
        "intervention.html",
        amount=amount,
        merchant=merchant,
        category=category,
        risk=risk_level,
        message=message
    )

@app.route("/confirm_payment", methods=["POST"])
def confirm_payment():
    global decisions_avoided
    
    amount = float(request.form["amount"])
    category = request.form["category"]
    risk = request.form["risk"]
    decision = request.form["decision"]
    
    if decision == "proceed":
        transactions.append({
            "amount": amount, 
            "category": category,
            "merchant": request.form.get("merchant", "Unknown")
        })
    else:
        if risk in ("medium", "high"):
            decisions_avoided += 1
    
    return redirect(url_for("dashboard"))

if __name__ == "__main__":
    app.run(debug=True, port=5000)
