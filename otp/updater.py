import subprocess
import sys
import threading
from importlib.metadata import version as pkg_version, PackageNotFoundError

import requests as _requests

PYPI_URL = "https://pypi.org/pypi/otp/json"


def _current_version():
    try:
        return pkg_version("otp")
    except PackageNotFoundError:
        return None


def _fetch_latest():
    try:
        r = _requests.get(PYPI_URL, timeout=3)
        r.raise_for_status()
        return r.json()["info"]["version"]
    except Exception:
        return None


def _do_upgrade():
    current = _current_version()
    latest = _fetch_latest()
    if current and latest and latest != current:
        print(f"  ↑ New version available ({current} → {latest}), upgrading...")
        try:
            subprocess.check_call(
                [sys.executable, "-m", "pip", "install", "--upgrade", "otp"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            print(f"  ✓ Upgraded to {latest}. Restart otp to use the new version.\n")
        except Exception:
            pass


def check_for_updates():
    t = threading.Thread(target=_do_upgrade, daemon=True)
    t.start()
    return t