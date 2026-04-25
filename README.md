# suk (single use key)

A tiny CLI that spins up a disposable email inbox in your terminal — handy for catching OTPs and verification codes without touching a browser.

<img width="596" height="184" alt="Screenshot" src="https://github.com/user-attachments/assets/b7837cab-e3d1-400b-b934-7e83872ce0a3" />


## Install

```bash
pip install suk
```

## Usage

```bash
suk            # use your saved inbox (auto-creates one on first run)
suk --new      # burn the old address and get a fresh one
suk --version  # print version
```

That's it. The email address is printed on startup, and any incoming message gets printed to the terminal in real-time (checks every 2 seconds).

Your inbox token is saved to `~/.otp_mailbox.json` so you keep the same address across sessions until you explicitly request a new one.

## Issues

For any issues, create an issue [here](https://github.com/forshaur/suk/issues)
## License

MIT
