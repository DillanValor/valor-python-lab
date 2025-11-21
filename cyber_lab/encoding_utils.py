#!/usr/bin/env python3
"""
Helpers for Base64, ROT13, XOR (CTF-style).
"""

import base64
from typing import Union


def b64_encode(s: str) -> str:
    return base64.b64encode(s.encode()).decode()


def b64_decode(s: str) -> str:
    return base64.b64decode(s.encode()).decode(errors="replace")


def rot13(s: str) -> str:
    result = []
    for ch in s:
        if "a" <= ch <= "z":
            result.append(chr((ord(ch) - ord("a") + 13) % 26 + ord("a")))
        elif "A" <= ch <= "Z":
            result.append(chr((ord(ch) - ord("A") + 13) % 26 + ord("A")))
        else:
            result.append(ch)
    return "".join(result)


def xor_bytes(data: bytes, key: Union[int, bytes]) -> bytes:
    if isinstance(key, int):
        return bytes([b ^ key for b in data])
    if isinstance(key, bytes):
        return bytes([b ^ key[i % len(key)] for i, b in enumerate(data)])
    raise TypeError("key must be int or bytes")


if __name__ == "__main__":
    s = "hello"
    print("Base64:", b64_encode(s))
    print("ROT13 :", rot13("pax8"))
    print("XOR   :", xor_bytes(b"test", 0x42))
