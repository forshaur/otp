"""
otp — disposable inbox in your terminal.

Usage:
    otp           use saved inbox (creates one if none exists)
    otp --new     burn the old address, get a fresh one
    otp --version print version and exit
"""

import sys

from otp import __version__
from otp.mail import create_mailbox, listen, load_saved_mailbox
from otp.updater import check_for_updates


def main():
    args = sys.argv[1:]

    if "--version" in args or "-v" in args:
        print(f"otp {__version__}")
        return

    # kick off update check early — it runs in the background
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

    # give the update thread a moment to print its message before we print ours
    update_thread.join(timeout=1.5)

    listen(token, mailbox)


if __name__ == "__main__":
    main()