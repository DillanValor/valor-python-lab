#!/usr/bin/env python3
"""
Domain audit tool skeleton.
Uses PowerShell under the hood to fetch AD info and writes JSON.
"""

import json
import subprocess
from datetime import datetime
from pathlib import Path


def run_ps(script: str) -> str:
    result = subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return result.stdout


def get_locked_out_users():
    ps = r"""
Import-Module ActiveDirectory
Search-ADAccount -LockedOut |
    Select-Object SamAccountName,Name,LockedOut,LastLogonDate |
    ConvertTo-Json
"""
    out = run_ps(ps)
    return json.loads(out) if out.strip() else []


def get_disabled_users():
    ps = r"""
Import-Module ActiveDirectory
Get-ADUser -Filter "Enabled -eq $false" -Properties SamAccountName,Name,Enabled,DistinguishedName |
    Select-Object SamAccountName,Name,Enabled,DistinguishedName |
    ConvertTo-Json
"""
    out = run_ps(ps)
    return json.loads(out) if out.strip() else []


def main():
    report = {
        "generated_at": datetime.now().isoformat(),
        "locked_out_users": get_locked_out_users(),
        "disabled_users": get_disabled_users(),
    }

    out_path = Path("domain_audit_report.json")
    out_path.write_text(json.dumps(report, indent=4), encoding="utf-8")
    print(f"[+] Report written to {out_path.resolve()}")


if __name__ == "__main__":
    main()
