#!/usr/bin/env python3
"""
Basic web scraping example: fetch a page and list all links.

Requires:
    pip install requests beautifulsoup4
"""

import requests
from bs4 import BeautifulSoup


def list_links(url: str) -> None:
    resp = requests.get(url, timeout=10)
    resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")
    for a in soup.find_all("a", href=True):
        print(a.get("href"))


if __name__ == "__main__":
    list_links("https://example.com")
