#!/usr/bin/env python3
"""
Very simple TCP client.
"""

import socket

HOST = "127.0.0.1"
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    s.sendall(b"Hello from client!")
    data = s.recv(1024)

print("Received:", data.decode(errors="replace"))
