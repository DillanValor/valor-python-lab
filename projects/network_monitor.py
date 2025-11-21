#!/usr/bin/env python3
"""
Very simple network monitor:
- Pings a list of hosts in a loop
- Prints when state changes (online -> offline, etc.)
"""

import subprocess
import time
from typing import Dict

HOSTS = {
    "DC01": "192.168.1.10",
    "FS01": "192.168.1.11",
    "FW01": "192.168.1.1",
}


def ping(ip: str) -> bool:
    result = subprocess.run(
        ["ping", "-n", "1", "-w", "500", ip],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def monitor(interval: int = 10) -> None:
    status: Dict[str, bool] = {}
    while True:
        for name, ip in HOSTS.items():
            is_up = ping(ip)
            old = status.get(name)
            status[name] = is_up
            if old is None:
                print(f"{name} ({ip}) is {'ONLINE' if is_up else 'offline'}")
            elif old != is_up:
                print(
                    f"[!] State change: {name} ({ip}) is now "
                    f"{'ONLINE' if is_up else 'offline'}"
                )
        time.sleep(interval)


if __name__ == "__main__":
    monitor(10)
