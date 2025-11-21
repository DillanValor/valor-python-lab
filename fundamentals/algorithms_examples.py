#!/usr/bin/env python3
"""
Simple algorithms implemented in pure Python.
"""


def bubble_sort(nums):
    nums = nums[:]  # copy
    n = len(nums)
    for i in range(n):
        for j in range(0, n - 1 - i):
            if nums[j] > nums[j + 1]:
                nums[j], nums[j + 1] = nums[j + 1], nums[j]
    return nums


def binary_search(sorted_list, target):
    """
    Return index of target in sorted_list or -1 if not found.
    """
    low, high = 0, len(sorted_list) - 1
    while low <= high:
        mid = (low + high) // 2
        value = sorted_list[mid]
        if value == target:
            return mid
        if value < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def caesar_cipher(text: str, shift: int) -> str:
    result = []
    for ch in text:
        if "a" <= ch <= "z":
            base = ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        elif "A" <= ch <= "Z":
            base = ord("A")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


if __name__ == "__main__":
    print("Bubble sort:", bubble_sort([5, 1, 4, 2, 8]))
    lst = [1, 3, 5, 7, 9]
    print("Binary search (5):", binary_search(lst, 5))
    print("Binary search (2):", binary_search(lst, 2))
    print("Caesar cipher:", caesar_cipher("Hello World", 3))
