# otp

A tiny CLI that spins up a disposable email inbox in your terminal — handy for catching OTPs and verification codes without touching a browser.
<img width="596" height="184" alt="Screenshot" src="https://github.com/user-attachments/assets/ec67a5b4-3e86-46d4-bcd7-5c35d03c57e8" />

## Install

```bash
pip install otp
```

## Usage

```bash
otp            # use your saved inbox (auto-creates one on first run)
otp --new      # burn the old address and get a fresh one
otp --version  # print version
```

That's it. The email address is printed on startup, and any incoming message gets printed to the terminal in real-time (checks every 2 seconds).

Your inbox token is saved to `~/.otp_mailbox.json` so you keep the same address across sessions until you explicitly request a new one.

## License

MIT
