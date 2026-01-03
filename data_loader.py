import csv

def load_transactions_from_csv(path="sample_data.csv"):
    transactions = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append({
                "date": row["date"],
                "time": row["time"],
                "merchant": row["merchant"],
                "amount": float(row["amount"]),
                "category": row["category"],
            })
    return transactions

if __name__ == "__main__":
    txns = load_transactions_from_csv()
    print(f"✅ Loaded {len(txns)} transactions")
    print("\nFirst 5:")
    for t in txns[:5]:
        print(f"  {t['date']} {t['time']} {t['merchant']} ₹{t['amount']} {t['category']}")
