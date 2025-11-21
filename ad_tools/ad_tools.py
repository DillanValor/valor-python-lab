#!/usr/bin/env python3
"""
ad_tools.py

Lightweight Python helper library for Active Directory automation using PowerShell.

Usage examples:

    from ad_tools import ADClient

    ad = ADClient(default_upn_suffix="yourdomain.local")

    ad.reset_password("jdoe", "TempP@ssw0rd123!", change_at_logon=True)
    ad.disable_user("jdoe")
    ad.enable_user("jdoe")
    ad.add_user_to_group("jdoe", "Helpdesk")
    ad.move_user("jdoe", "OU=Terminated,OU=Users,DC=yourdomain,DC=local")

    locked = ad.get_locked_out_users()
    for u in locked:
        print(u["SamAccountName"], u["LastLogonDate"])
"""

from __future__ import annotations

import json
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional


def _escape_ps_single_quotes(value: str) -> str:
    """Escape single quotes for use in single-quoted PowerShell strings."""
    return value.replace("'", "''")


def _run_powershell(script: str) -> subprocess.CompletedProcess:
    """Run a PowerShell script and return the CompletedProcess."""
    return subprocess.run(
        ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-Command", script],
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def _run_ps_json(script: str, depth: int = 5) -> Any:
    """
    Run a PowerShell script that ends with ConvertTo-Json
    and return parsed JSON.
    """
    wrapped = f"{script.strip()}\n| ConvertTo-Json -Depth {depth}"
    result = _run_powershell(wrapped)

    if result.returncode != 0:
        raise RuntimeError(f"PowerShell error: {result.stderr.strip()}")

    output = result.stdout.strip()
    if not output:
        return None

    try:
        return json.loads(output)
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse JSON from PowerShell:\n{output}") from e


@dataclass
class ADClient:
    """
    High-level helper for common AD operations using PowerShell.

    Attributes:
        default_upn_suffix: Used for UPN when creating users, e.g. 'yourdomain.local'
    """

    default_upn_suffix: Optional[str] = None

    # ---------- User lookup / info ----------

    def find_user(self, identity: str) -> Optional[Dict[str, Any]]:
        """
        Find a user by samAccountName or UPN.
        Returns a dict of AD user properties or None if not found.
        """
        identity_escaped = _escape_ps_single_quotes(identity)

        ps = f"""
Import-Module ActiveDirectory

$user = Get-ADUser -Filter "SamAccountName -eq '{identity_escaped}' -or UserPrincipalName -eq '{identity_escaped}'" -Properties *
if ($user -eq $null) {{
    return
}}
$user
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            if "Cannot find an object with identity" in result.stderr:
                return None
            raise RuntimeError(f"PowerShell error: {result.stderr.strip()}")

        output = result.stdout.strip()
        if not output:
            return None

        # Return as JSON via a second call to keep parsing simple
        ps_json = f"""
Import-Module ActiveDirectory
$user = Get-ADUser -Filter "SamAccountName -eq '{identity_escaped}' -or UserPrincipalName -eq '{identity_escaped}'" -Properties *
$user
"""
        return _run_ps_json(ps_json)

    def get_user_dn(self, identity: str) -> Optional[str]:
        """Return distinguishedName for given identity, or None if not found."""
        identity_escaped = _escape_ps_single_quotes(identity)

        ps = f"""
Import-Module ActiveDirectory
$user = Get-ADUser -Filter "SamAccountName -eq '{identity_escaped}' -or UserPrincipalName -eq '{identity_escaped}'" -Properties DistinguishedName
if ($user -eq $null) {{
    return
}}
$user.DistinguishedName
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            if "Cannot find an object with identity" in result.stderr:
                return None
            raise RuntimeError(f"PowerShell error: {result.stderr.strip()}")

        dn = result.stdout.strip()
        return dn or None

    # ---------- Password operations ----------

    def reset_password(
        self,
        identity: str,
        new_password: str,
        change_at_logon: bool = True,
    ) -> None:
        """Reset a user's password and optionally force change at next logon."""
        identity_escaped = _escape_ps_single_quotes(identity)
        pw_escaped = _escape_ps_single_quotes(new_password)

        ps = f"""
Import-Module ActiveDirectory
Set-ADAccountPassword -Identity '{identity_escaped}' -Reset -NewPassword (ConvertTo-SecureString '{pw_escaped}' -AsPlainText -Force)
"""
        if change_at_logon:
            ps += f"""
Set-ADUser -Identity '{identity_escaped}' -ChangePasswordAtLogon $true
"""

        result = _run_powershell(ps)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to reset password: {result.stderr.strip()}")

    def unlock_user(self, identity: str) -> None:
        """Unlock a locked AD account."""
        identity_escaped = _escape_ps_single_quotes(identity)

        ps = f"""
Import-Module ActiveDirectory
Unlock-ADAccount -Identity '{identity_escaped}'
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to unlock user: {result.stderr.strip()}")

    # ---------- Enable / disable / move ----------

    def disable_user(self, identity: str) -> None:
        """Disable a user account."""
        identity_escaped = _escape_ps_single_quotes(identity)

        ps = f"""
Import-Module ActiveDirectory
Disable-ADAccount -Identity '{identity_escaped}'
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to disable user: {result.stderr.strip()}")

    def enable_user(self, identity: str) -> None:
        """Enable a user account."""
        identity_escaped = _escape_ps_single_quotes(identity)

        ps = f"""
Import-Module ActiveDirectory
Enable-ADAccount -Identity '{identity_escaped}'
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to enable user: {result.stderr.strip()}")

    def move_user(self, identity: str, target_ou_dn: str) -> None:
        """
        Move a user to a different OU.
        target_ou_dn must be a valid OU DN (e.g., 'OU=Users,DC=yourdomain,DC=local')
        """
        identity_escaped = _escape_ps_single_quotes(identity)
        ou_escaped = _escape_ps_single_quotes(target_ou_dn)

        ps = f"""
Import-Module ActiveDirectory
Move-ADObject -Identity '{identity_escaped}' -TargetPath '{ou_escaped}'
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            raise RuntimeError(f"Failed to move user: {result.stderr.strip()}")

    # ---------- Group operations ----------

    def add_user_to_group(self, identity: str, group: str) -> None:
        """Add a user to a group."""
        user_escaped = _escape_ps_single_quotes(identity)
        group_escaped = _escape_ps_single_quotes(group)

        ps = f"""
Import-Module ActiveDirectory
Add-ADGroupMember -Identity '{group_escaped}' -Members '{user_escaped}'
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to add user to group: {result.stderr.strip()}"
            )

    def remove_user_from_group(self, identity: str, group: str) -> None:
        """Remove a user from a group."""
        user_escaped = _escape_ps_single_quotes(identity)
        group_escaped = _escape_ps_single_quotes(group)

        ps = f"""
Import-Module ActiveDirectory
Remove-ADGroupMember -Identity '{group_escaped}' -Members '{user_escaped}' -Confirm:$false
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to remove user from group: {result.stderr.strip()}"
            )

    # ---------- Reporting / queries ----------

    def get_locked_out_users(self) -> List[Dict[str, Any]]:
        """Return a list of locked-out users as dicts."""
        ps = """
Import-Module ActiveDirectory
Search-ADAccount -LockedOut |
    Select-Object SamAccountName,Name,LockedOut,LastLogonDate
"""
        result = _run_ps_json(ps, depth=4)
        if result is None:
            return []
        if isinstance(result, dict):
            return [result]
        return result

    def get_disabled_users(self) -> List[Dict[str, Any]]:
        """Return a list of disabled users."""
        ps = """
Import-Module ActiveDirectory
Get-ADUser -Filter "Enabled -eq $false" -Properties SamAccountName,Name,Enabled,DistinguishedName |
    Select-Object SamAccountName,Name,Enabled,DistinguishedName
"""
        result = _run_ps_json(ps, depth=4)
        if result is None:
            return []
        if isinstance(result, dict):
            return [result]
        return result

    # ---------- Bulk operations ----------

    def bulk_create_users_from_csv(
        self,
        csv_path: str | Path,
        default_password: str,
        upn_suffix: Optional[str] = None,
        enable: bool = True,
    ) -> None:
        """
        Bulk create users from a CSV using PowerShell's Import-Csv + New-ADUser.

        CSV columns:
            SamAccountName, GivenName, Surname, OU
        Optional:
            DisplayName, Department, Title, Office, Email
        """
        csv_path = Path(csv_path).resolve()
        if not csv_path.exists():
            raise FileNotFoundError(csv_path)

        pw_esc = _escape_ps_single_quotes(default_password)
        upn_suffix = upn_suffix or self.default_upn_suffix

        if upn_suffix:
            upn_suffix_escaped = _escape_ps_single_quotes(upn_suffix)
            upn_expr = (
                f"$upn = \"$($row.SamAccountName)@{upn_suffix_escaped}\""
            )
        else:
            upn_expr = "$upn = $null"

        ps = f"""
Import-Module ActiveDirectory
$csvPath = '{_escape_ps_single_quotes(str(csv_path))}'
$defaultPassword = ConvertTo-SecureString '{pw_esc}' -AsPlainText -Force

Import-Csv -Path $csvPath | ForEach-Object {{
    $row = $_
    {upn_expr}

    $displayName = if ($row.DisplayName) {{ $row.DisplayName }} else {{ "$($row.GivenName) $($row.Surname)" }}

    New-ADUser `
        -SamAccountName $row.SamAccountName `
        -GivenName $row.GivenName `
        -Surname $row.Surname `
        -Name $displayName `
        -UserPrincipalName $upn `
        -Path $row.OU `
        -Department $row.Department `
        -Title $row.Title `
        -Office $row.Office `
        -EmailAddress $row.Email `
        -AccountPassword $defaultPassword `
        -Enabled ${str(enable).lower()}
}}
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            raise RuntimeError(
                f"Bulk create failed: {result.stderr.strip()}"
            )

    # ---------- Convenience helpers ----------

    def create_user(
        self,
        sam_account_name: str,
        given_name: str,
        surname: str,
        ou_dn: str,
        password: str,
        department: Optional[str] = None,
        title: Optional[str] = None,
        office: Optional[str] = None,
        email: Optional[str] = None,
        enabled: bool = True,
    ) -> None:
        """Create a single AD user with common attributes."""
        sam_esc = _escape_ps_single_quotes(sam_account_name)
        given_esc = _escape_ps_single_quotes(given_name)
        sur_esc = _escape_ps_single_quotes(surname)
        ou_esc = _escape_ps_single_quotes(ou_dn)
        pw_esc = _escape_ps_single_quotes(password)
        dept_esc = _escape_ps_single_quotes(department) if department else ""
        title_esc = _escape_ps_single_quotes(title) if title else ""
        office_esc = _escape_ps_single_quotes(office) if office else ""
        email_esc = _escape_ps_single_quotes(email) if email else ""

        if self.default_upn_suffix:
            upn = f"{sam_account_name}@{self.default_upn_suffix}"
        else:
            upn = ""
        upn_esc = _escape_ps_single_quotes(upn)

        display_name = f"{given_name} {surname}"
        display_esc = _escape_ps_single_quotes(display_name)

        ps = f"""
Import-Module ActiveDirectory

$pwd = ConvertTo-SecureString '{pw_esc}' -AsPlainText -Force

New-ADUser `
    -SamAccountName '{sam_esc}' `
    -GivenName '{given_esc}' `
    -Surname '{sur_esc}' `
    -Name '{display_esc}' `
    -UserPrincipalName '{upn_esc}' `
    -Path '{ou_esc}' `
    -Department '{dept_esc}' `
    -Title '{title_esc}' `
    -Office '{office_esc}' `
    -EmailAddress '{email_esc}' `
    -AccountPassword $pwd `
    -Enabled ${str(enabled).lower()}
"""
        result = _run_powershell(ps)
        if result.returncode != 0:
            raise RuntimeError(
                f"Failed to create user: {result.stderr.strip()}"
            )
