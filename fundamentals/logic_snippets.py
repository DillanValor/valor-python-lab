#!/usr/bin/env python3
"""
Small logic examples for practice.
"""

from collections import Counter


def reverse_string(s: str) -> str:
    return s[::-1]


def count_vowels(s: str) -> int:
    vowels = set("aeiouAEIOU")
    return sum(1 for ch in s if ch in vowels)


def find_duplicates(items):
    c = Counter(items)
    return [item for item, count in c.items() if count > 1]


def sort_dict_by_value(d: dict) -> list:
    return sorted(d.items(), key=lambda kv: kv[1])


if __name__ == "__main__":
    print(reverse_string("Valor"))
    print(count_vowels("Dillan Valor"))
    print(find_duplicates([1, 2, 2, 3, 3, 3, 4]))
    print(sort_dict_by_value({"a": 3, "b": 1, "c": 2}))
