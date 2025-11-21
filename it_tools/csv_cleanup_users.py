#!/usr/bin/env python3
"""
Read a CSV of users and normalize data:
- Trim spaces
- Lowercase emails
- Print a report of duplicate emails
"""

import csv
from collections import Counter
from pathlib import Path


def clean_users(csv_path: str) -> None:
    path = Path(csv_path)
    if not path.is_file():
        print(f"[!] File not found: {path}")
        return

    users = []
    with path.open("r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = (row.get("Email") or "").strip().lower()
            name = (row.get("Name") or "").strip()
            dept = (row.get("Department") or "").strip()
            users.append({"Name": name, "Email": email, "Department": dept})

    email_counts = Counter(u["Email"] for u in users if u["Email"])
    dupes = [email for email, count in email_counts.items() if count > 1]

    print("=== Duplicate emails ===")
    if not dupes:
        print("No duplicates found.")
        return

    for email in dupes:
        print(email)
        for u in users:
            if u["Email"] == email:
                print(f"  - {u['Name']} ({u['Department']})")


if __name__ == "__main__":
    clean_users("users.csv")
