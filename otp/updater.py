"""
Auto-upgrade helper. Checks PyPI for a newer version and re-installs if found.
Runs silently in the background on every invocation.
"""

import subprocess
import sys
import threading

import requests as _requests

from otp import __version__

PYPI_URL = "https://pypi.org/pypi/otp/json"


def _fetch_latest():
    try:
        r = _requests.get(PYPI_URL, timeout=3)
        r.raise_for_status()
        return r.json()["info"]["version"]
    except Exception:
        return None


def _do_upgrade():
    latest = _fetch_latest()
    if latest and latest != __version__:
        print(f"  ↑ New version available ({__version__} → {latest}), upgrading...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", "otp"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"  ✓ Upgraded to {latest}. Restart otp to use the new version.\n")
        except Exception:
            pass  # non-fatal, carry on


def check_for_updates():
    """Fire off the update check in a daemon thread so it doesn't block startup."""
    t = threading.Thread(target=_do_upgrade, daemon=True)
    t.start()
    return t