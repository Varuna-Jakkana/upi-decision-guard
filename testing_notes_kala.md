\# UPI Decision Guard – Testing Notes (Kala)



\## Sample Data

\- `sample\_data.csv`: 18 transactions loaded successfully

\- Categories: Food(9), Travel(4), Entertainment(5)

\- Late night (>23:00): 4 transactions (SWIGGY 23:30, ZOMATO 00:15, SWIGGY 00:45, MC DONALDS 01:10)



\## Test Plan



\### Test 1 – Setup

\*\*Steps:\*\* /setup → Budget 8000, Food 3000, Travel 2000, Entertainment 1000 → Dashboard  

\*\*Expected:\*\* Budget/limits show correctly  

\*\*Result:\*\* ☐ PASS ☐ FAIL  

\*\*Notes:\*\*



\### Test 2 – Low Risk (Morning coffee)

\*\*Steps:\*\* Add Payment → ₹220 STARBUCKS Food 09:10 → Proceed  

\*\*Expected:\*\* Risk LOW, Food total +220  

\*\*Result:\*\* ☐ PASS ☐ FAIL  

\*\*Notes:\*\*



\### Test 3 – High Risk (Late night binge)

\*\*Steps:\*\* Add 4 Food payments: 23:30 SWIGGY ₹450, 00:15 ZOMATO ₹300, 00:45 SWIGGY ₹350, 01:10 MC DONALDS ₹400  

\*\*Expected:\*\* 3rd/4th → HIGH risk, Cancel → decisions\_avoided +1  

\*\*Result:\*\* ☐ PASS ☐ FAIL  

\*\*Notes:\*\*



\### Test 4 – Medium Risk (Near limit)

\*\*Steps:\*\* Food limit 1000 → Add ₹400+₹300=700 → Add ₹200 → Risk MEDIUM  

\*\*Expected:\*\* Food 900/1000 warning  

\*\*Result:\*\* ☐ PASS ☐ FAIL  

\*\*Notes:\*\*



\### Test 5 – Dashboard Totals

\*\*Steps:\*\* After multiple "Proceed" → Check totals match  

\*\*Expected:\*\* Dashboard = manual sum  

\*\*Result:\*\* ☐ PASS ☐ FAIL  

\*\*Notes:\*\*



\## Demo Scenarios (for Varuna/Team)

1\. Safe coffee ☕ (Test 2)

2\. Late night binge 🌙 (Test 3) 

3\. Budget warning ⚠️ (Test 4)



