import json
import sys
import time
from pathlib import Path

from curl_cffi import requests

DATA_FILE = Path.home() / ".otp_mailbox.json"

# ANSI colors
CYAN   = "\033[96m"
GREEN  = "\033[92m"
YELLOW = "\033[93m"
BOLD   = "\033[1m"
RESET  = "\033[0m"

HEADERS_BASE = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:149.0) Gecko/20100101 Firefox/149.0",
    "Accept": "*/*",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Referer": "https://temp-mail.org/",
    "Origin": "https://temp-mail.org",
    "Connection": "keep-alive",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Priority": "u=4",
    "TE": "trailers",
}


def _post_headers():
    return {**HEADERS_BASE, "Content-Type": "application/json", "Content-Length": "0"}


def _auth_headers(token):
    return {**HEADERS_BASE, "Authorization": f"Bearer {token}"}


def create_mailbox():
    """Hit the API, get a fresh mailbox, stash the creds locally."""
    print("Spinning up a new inbox...")

    try:
        r = requests.post(
            "https://web2.temp-mail.org/mailbox",
            headers=_post_headers(),
            impersonate="firefox",
        )
        r.raise_for_status()
    except Exception as e:
        print(f"Couldn't reach temp-mail: {e}")
        sys.exit(1)

    data = r.json()
    DATA_FILE.write_text(json.dumps(data, indent=2))
    return data["token"], data["mailbox"]


def load_saved_mailbox():
    """Pull creds from the local stash. Returns (token, mailbox) or None."""
    if not DATA_FILE.exists():
        return None
    try:
        data = json.loads(DATA_FILE.read_text())
        token = data.get("token")
        mailbox = data.get("mailbox")
        if token and mailbox:
            return token, mailbox
    except Exception:
        pass
    return None


def listen(token, mailbox):
    """Poll the inbox every 2s and print anything new."""
    print(f"\n  Email  →  {BOLD}{CYAN}{mailbox}{RESET}")
    print(f"  Waiting for messages... (Ctrl+C to quit)\n")

    seen = set()

    try:
        while True:
            try:
                r = requests.get(
                    "https://web2.temp-mail.org/messages",
                    headers=_auth_headers(token),
                    impersonate="firefox",
                )
            except Exception:
                time.sleep(3)
                continue

            if r.status_code in (401, 403):
                print("Session expired. Run `otp --new` to get a fresh address.")
                break

            if r.status_code == 200:
                for msg in r.json().get("messages", []):
                    mid = msg.get("_id")
                    if mid not in seen:
                        seen.add(mid)
                        _print_message(msg)

            time.sleep(2)

    except KeyboardInterrupt:
        print("\nDone.")


def _print_message(msg):
    print(f"{YELLOW}{'─' * 52}{RESET}")
    print(f"  {BOLD}From{RESET}    : {msg.get('from', '—')}")
    print(f"  {BOLD}Subject{RESET} : {GREEN}{msg.get('subject', '(no subject)')}{RESET}")
    print(f"  {BOLD}Preview{RESET} : {msg.get('bodyPreview', '').strip()}")
    print(f"{YELLOW}{'─' * 52}{RESET}\n")