#!/usr/bin/env python3
"""
Simple functions to illustrate inputs/outputs.
"""


def sum_list(values):
    total = 0
    for v in values:
        total += v
    return total


def is_palindrome(word: str) -> bool:
    cleaned = word.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def factorial(n: int) -> int:
    if n < 0:
        raise ValueError("n must be non-negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    print(sum_list([1, 2, 3]))
    print(is_palindrome("racecar"))
    print(is_palindrome("Valor"))
    print(factorial(5))
