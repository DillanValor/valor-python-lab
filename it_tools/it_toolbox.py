#!/usr/bin/env python3
"""
Simple IT toolbox with subcommands (ping-subnet, find-large-files).

Usage examples:
    python it_tools/it_toolbox.py ping-subnet 192.168.1.0/24
    python it_tools/it_toolbox.py find-large-files C:\ --min-mb 500
"""

import argparse
import os
import subprocess
from pathlib import Path


def ping_subnet(subnet: str) -> None:
    import ipaddress

    net = ipaddress.ip_network(subnet, strict=False)
    for ip in net.hosts():
        ip_str = str(ip)
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "500", ip_str],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        status = "ONLINE" if result.returncode == 0 else "offline"
        print(f"{ip_str:15} {status}")


def find_large_files(path: str, min_mb: int) -> None:
    root = Path(path)
    min_bytes = min_mb * 1024 * 1024

    for folder, _, files in os.walk(root):
        for name in files:
            file_path = Path(folder) / name
            try:
                size = file_path.stat().st_size
            except OSError:
                continue

            if size >= min_bytes:
                print(f"{size/1024/1024:8.1f} MB  {file_path}")


def main():
    parser = argparse.ArgumentParser(description="IT Toolbox")
    subparsers = parser.add_subparsers(dest="command")

    ping_parser = subparsers.add_parser("ping-subnet")
    ping_parser.add_argument("subnet", help="e.g., 192.168.1.0/24")

    large_parser = subparsers.add_parser("find-large-files")
    large_parser.add_argument("path", help="Root directory to scan")
    large_parser.add_argument(
        "--min-mb", type=int, default=500, help="Min size in MB"
    )

    args = parser.parse_args()

    if args.command == "ping-subnet":
        ping_subnet(args.subnet)
    elif args.command == "find-large-files":
        find_large_files(args.path, args.min_mb)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
