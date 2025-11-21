#!/usr/bin/env python3
"""
Password helper:
- Generate random passwords
- Check "strength" (very basic)
- Hash with SHA-256
"""

import hashlib
import random
import string


def generate_password(length: int = 16) -> str:
    chars = string.ascii_letters + string.digits + "!@#$%^&*()-_=+"
    return "".join(random.choice(chars) for _ in range(length))


def password_strength(pw: str) -> int:
    score = 0
    if len(pw) >= 8:
        score += 1
    if any(c.islower() for c in pw):
        score += 1
    if any(c.isupper() for c in pw):
        score += 1
    if any(c.isdigit() for c in pw):
        score += 1
    if any(c in "!@#$%^&*()-_=+" for c in pw):
        score += 1
    return score  # 0–5


def sha256_hash(pw: str) -> str:
    return hashlib.sha256(pw.encode()).hexdigest()


if __name__ == "__main__":
    pw = generate_password()
    print("Password:", pw)
    print("Strength score (0-5):", password_strength(pw))
    print("SHA256:", sha256_hash(pw))
