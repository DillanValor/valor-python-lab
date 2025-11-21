#!/usr/bin/env python3
"""
Practice loops with different kinds of data.
"""


def every_third(items):
    for i in range(0, len(items), 3):
        print(f"Index {i}: {items[i]}")


def print_errors(lines):
    for line in lines:
        if "error" in line.lower():
            print(line.strip())


def print_big_values(d: dict, threshold: int):
    for key, value in d.items():
        if isinstance(value, (int, float)) and value > threshold:
            print(f"{key}: {value}")


if __name__ == "__main__":
    every_third(["a", "b", "c", "d", "e", "f", "g"])
    print_errors(["ok", "Error: bad", "warning", "Critical error occurred"])
    print_big_values({"a": 5, "b": 20, "c": 3, "d": 50}, 10)
