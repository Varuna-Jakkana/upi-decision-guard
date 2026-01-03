# UPI Decision Guard

## Overview

UPI payments in India are fast and frictionless, which makes it very easy to overspend on small, frequent, and emotionally-driven transactions. Existing apps usually show spending summaries only after the money is already gone, or they use static limits that do not adapt to a user’s behavior.[web:31][web:32]

**UPI Decision Guard** is a behavioral finance–based pre-payment intervention system. Instead of just tracking expenses, it analyzes a user’s spending patterns and gently intervenes at the moment of a risky UPI payment with a “pause moment” and smart nudges.

---

## Problem

- People overspend on UPI because payments are instant and feel “less real” than cash.[web:29][web:34]  
- Current tools focus on monthly reports and budgets, not on the decision moment.  
- There is no simple system that detects impulse patterns (late-night orders, repeated micro-payments, near-limit spending) and asks the user to reconsider before paying.

---

## Solution

UPI Decision Guard runs a lightweight risk engine whenever a user logs a new UPI payment:

- Checks **time** (late night / risky hours).  
- Checks **frequency** (how many similar payments today).  
- Checks **budget usage** (how close to category limit).  
- If risk is high, shows a **Pause Moment** screen with context and two choices:
  - “Proceed anyway”
  - “Cancel & Save”

If the user cancels, the app counts it as a **decision avoided** and estimates potential savings.

This turns budgeting from passive (after spending) to active, behavior-aware decision support.

---

## Features (MVP)

- Budget and category setup (Food, Travel, Entertainment, etc.).  
- Add UPI payments manually (amount, merchant, category, time).  
- Risk calculation for each new payment based on time, frequency, and budget usage.  
- Intervention popup with Proceed / Cancel choice.  
- Dashboard with:
  - Total spent vs budget  
  - Category-wise spending  
  - Number of decisions avoided  
  - Estimated money saved

---

## Tech Stack

- **Backend & Web Framework:** Python + Flask[web:54]  
- **Frontend:** HTML5 + CSS (Jinja templates rendered by Flask)  
- **Data:** In-memory list and sample CSV (`sample_data.csv`) for demo  
- **Tools:** GitHub for collaboration, (optionally) Google Firebase / Firestore for future storage[web:52][web:61]

---

## Project Structure

```text
upi-decision-guard/
│
├─ app.py              # Flask app with routes
├─ risk_engine.py      # Risk calculation logic
├─ data_loader.py      # Helper to load sample_data.csv (test data)
├─ sample_data.csv     # 18+ realistic UPI transactions (Food/Travel/Entertainment)
│
├─ templates/
│   ├─ base.html
│   ├─ setup.html
│   ├─ dashboard.html
│   ├─ add_payment.html
│   ├─ intervention.html
│   └─ login.html
│
├─ static/
│   └─ styles.css
│
└─ README.md
