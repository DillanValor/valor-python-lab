#!/usr/bin/env python3
"""
Simple log analyzer:
- Counts occurrences of "error", "warning", "info"
"""

from collections import Counter
from pathlib import Path


def analyze_log(path: str):
    p = Path(path)
    if not p.is_file():
        print(f"[!] File not found: {p}")
        return

    counts = Counter()
    with p.open("r", encoding="utf-8", errors="ignore") as f:
        for line in f:
            lower = line.lower()
            if "error" in lower:
                counts["error"] += 1
            if "warning" in lower:
                counts["warning"] += 1
            if "info" in lower:
                counts["info"] += 1

    print("=== Log Summary ===")
    for level in ["error", "warning", "info"]:
        print(f"{level:7}: {counts[level]}")


if __name__ == "__main__":
    analyze_log(r"C:\Logs\app.log")
