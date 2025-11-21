# Valor Python Lab

A collection of practical Python scripts and mini-projects focused on:

- IT / MSP automation
- Active Directory tooling
- Cyber / CTF practice
- Core Python fundamentals

See folders for full examples.

## 📚 How & When to Use Each Folder

This repo is meant to be both a toolbox and a learning lab.  
Here’s how to think about each folder, when to use the scripts inside it, and what you’ll get out of them.

---

### 🧰 `it_tools/` – Day-to-day IT / MSP Stuff

These are the scripts you’d reach for while working tickets or reviewing systems.

#### `it_toolbox.py`
**What it is:** A small command-line “Swiss Army knife” with subcommands.  
**When to use:**
- You need to quickly ping a subnet.
- You want to find large files on a drive.

**Examples:**
```bash
# Ping every host in a subnet
python it_tools/it_toolbox.py ping-subnet 192.168.1.0/24

# Find files bigger than 1GB under C:\
python it_tools/it_toolbox.py find-large-files C:\ --min-mb 1024

parse_failed_logins.py

What it is: Simple log parser that finds lines containing "failed" (case-insensitive).
When to use:

Looking through security logs for failed logons.

Reviewing app logs for failed connections/auth attempts.

Example:

python it_tools/parse_failed_logins.py
# (edit the default path in the script, or extend with argparse)

csv_cleanup_users.py

What it is: Cleans a CSV of users and finds duplicate emails.
When to use:

Cleaning up exported user lists from HR/AD/other systems.

Preparing a CSV for bulk import (AD, M365, etc.).

Example:

python it_tools/csv_cleanup_users.py
# expects users.csv in repo root by default

ping_subnet.py

What it is: Fast “is anything alive in this /24?” script.
When to use:

Checking which hosts are online during troubleshooting.

Getting a quick feel for which IPs are in use in a small subnet.

Example:

python it_tools/ping_subnet.py
# edit subnet inside the script or adapt it to take CLI args

log_analyzer.py

What it is: Counts how many times error, warning, and info show up in a log.
When to use:

Quick triage on a big log file.

Getting a high-level view before deeper analysis.

Example:

python it_tools/log_analyzer.py
# edit the path in the script to point to your log

🧾 ad_tools/ – Active Directory Automation

These scripts assume Windows + PowerShell + ActiveDirectory module.

ad_tools.py

What it is: A Python library that wraps common AD PowerShell commands in an ADClient class.
When to use:

You want Python logic + AD actions (reset password, disable user, move to OU, etc.).

You’re building bigger tools or automations that will touch AD.

Typical pattern:

from ad_tools import ADClient

ad = ADClient(default_upn_suffix="yourdomain.local")

ad.reset_password("jdoe", "TempP@ssw0rd123!", change_at_logon=True)
ad.disable_user("jdoe")
ad.add_user_to_group("jdoe", "Helpdesk")


Use this file as a library, not a script: import it into other Python files.

domain_audit_tool.py

What it is: A script that queries AD (via PowerShell) and writes a JSON “audit” report.
When to use:

You want a quick snapshot of locked-out and disabled users.

You’re building reports / dashboards and need a data source.

Example:

python ad_tools/domain_audit_tool.py
# -> creates domain_audit_report.json in the repo root

🧪 cyber_lab/ – CTF, Pentest, and Lab Toys

These are practice tools to make CTFs and homelab experiments easier.

encoding_utils.py

What it is: Helpers for Base64, ROT13, and XOR operations.
When to use:

Working on CTFs that involve weird encodings.

Quickly experimenting with simple cryptography/obfuscation.

Example (interactive use):

python cyber_lab/encoding_utils.py
# or import:
from cyber_lab.encoding_utils import b64_decode, rot13, xor_bytes

tcp_server.py & tcp_client.py

What they are: Very small TCP echo server + client.
When to use:

Practicing basic networking with sockets.

Testing firewall rules, port forwarding, or simple connectivity.

Examples:

# Terminal 1
python cyber_lab/tcp_server.py

# Terminal 2
python cyber_lab/tcp_client.py

simple_scraper.py

What it is: Minimal web scraper using requests + BeautifulSoup.
When to use:

Pulling all links from a page.

Practicing HTTP + HTML parsing.

Example:

python cyber_lab/simple_scraper.py
# edit the URL inside the script or extend with argparse


Requires:

pip install requests beautifulsoup4

📘 fundamentals/ – Pure Python Practice

These files aren’t “tools” so much as skill-building exercises.

logic_snippets.py

What it covers:
String reversing, vowel counting, duplicate detection, dict sorting.

When to use:

Warming up your brain before working on “real” scripts.

Practicing reading and modifying small, pure-Python functions.

functions_examples.py

What it covers:
Functions, arguments, return values, simple error handling.

When to use:

Practicing how to define and call functions.

Playing with refactors (e.g., change logic, add parameters).

loop_examples.py

What it covers:
Different loop patterns over lists, text, and dicts.

When to use:

Getting comfortable iterating through data structures.

Translating “I need to go through X and pick out Y” into code.

algorithms_examples.py

What it covers:
Bubble sort, binary search, and a Caesar cipher.

When to use:

Practicing step-by-step logic and thinking like the interpreter.

Getting more comfortable with indexes, conditions, and math in code.

🧩 projects/ – Small but Real Tools

These are “mini-projects” that feel closer to real workflows.

password_toolkit.py

What it is: Password generator + basic strength checker + SHA-256 hasher.
When to use:

You need strong random passwords for lab accounts.

You want to experiment with password policies and hashing.

Example:

python projects/password_toolkit.py


Try modifying:

The character set

Minimum strength requirement

Output format (e.g., JSON or clipboard)

network_monitor.py

What it is: Very simple ping monitor for a few critical hosts.
When to use:

Lab-style “up/down” monitor for servers, firewall, etc.

Practicing state tracking and loops over time.

Example:

python projects/network_monitor.py
# Edit HOSTS dict in the file with your own IPs


Ideas to extend:

Log state changes to a file.

Add email/Teams/Webhook alerts.

Serve a tiny web page showing the current status.

🧠 How to Practice With This Repo

Pick a script from any folder.

Run it once as-is so you see what it does.

Then try one of these changes:

Add argparse so it accepts arguments from the command line.

Add logging to a file.

Add error handling (bad paths, permissions, network failures).

Turn copy-pasted values (paths, domains, IPs) into config variables.

Use fundamentals/ to build raw Python skill,
it_tools/ + ad_tools/ to improve real-world automation,
and cyber_lab/ + projects/ to have fun and explore.
