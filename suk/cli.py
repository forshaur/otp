"""
suk — disposable inbox in your terminal.

Usage:
    suk           use saved inbox (creates one if none exists)
    suk --new     burn the old address, get a fresh one
    suk --version print version and exit
"""

import sys
from importlib.metadata import version as pkg_version, PackageNotFoundError

from suk.mail import create_mailbox, listen, load_saved_mailbox
from suk.updater import check_for_updates


def _get_version():
    try:
        return pkg_version("suk")
    except PackageNotFoundError:
        return "unknown"


def main():
    args = sys.argv[1:]

    if "--version" in args or "-v" in args:
        print(f"suk {_get_version()}")
        return

    update_thread = check_for_updates()

    if "--new" in args or "-n" in args:
        token, mailbox = create_mailbox()
    else:
        saved = load_saved_mailbox()
        if saved:
            token, mailbox = saved
        else:
            print("No saved inbox found, creating one...")
            token, mailbox = create_mailbox()

    update_thread.join(timeout=1.5)
    listen(token, mailbox)


if __name__ == "__main__":
    main()