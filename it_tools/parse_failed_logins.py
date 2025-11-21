#!/usr/bin/env python3
"""
Scan a log file for lines containing the word "failed" (case-insensitive)
and print them with line numbers.
"""

from pathlib import Path


def find_failed_lines(log_path: str) -> None:
    path = Path(log_path)
    if not path.is_file():
        print(f"[!] File not found: {path}")
        return

    with path.open("r", encoding="utf-8", errors="ignore") as f:
        for lineno, line in enumerate(f, start=1):
            if "failed" in line.lower():
                print(f"{lineno:6}: {line.rstrip()}")


if __name__ == "__main__":
    # Change this path or add argparse if you want CLI args
    log_file = r"C:\Logs\security.log"
    find_failed_lines(log_file)
