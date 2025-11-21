#!/usr/bin/env python3
"""
Very simple TCP echo server.
"""

import socket

HOST = "0.0.0.0"
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(5)
    print(f"[+] Listening on {HOST}:{PORT}...")
    while True:
        conn, addr = s.accept()
        with conn:
            print(f"[+] Connection from {addr}")
            data = conn.recv(1024)
            if not data:
                continue
            print("[>] Received:", data.decode(errors="replace"))
            conn.sendall(b"Echo: " + data)
