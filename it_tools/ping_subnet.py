#!/usr/bin/env python3
"""
Ping all IPs in a /24 subnet on Windows and print which respond.

Example:
    python it_tools/ping_subnet.py
"""

import ipaddress
import subprocess


def ping_host(ip: str) -> bool:
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "500", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def ping_subnet(subnet: str) -> None:
    net = ipaddress.ip_network(subnet, strict=False)
    for ip in net.hosts():
        ip_str = str(ip)
        is_up = ping_host(ip_str)
        print(f"{ip_str:15} {'ONLINE' if is_up else 'offline'}")


if __name__ == "__main__":
    ping_subnet("192.168.1.0/24")
