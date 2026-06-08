# 🔐 Alohomora

RSA file & directory encryptor with a Rich terminal UI.  
Works on **Linux**, **Windows**, and **Termux (Android)**.

---

## Install

```bash
pip install -r requirements.txt
```

On Termux:
```bash
pkg install python
pip install -r requirements.txt
```

---

## Run

```bash
python alohomora.py
```

---

## Key loading — env vars (recommended)

Set these before running to load keys from a custom location:

```bash
# Linux / Termux
export ALOHOMORA_PRIVATE_KEY="/path/to/private.pem"
export ALOHOMORA_PUBLIC_KEY="/path/to/public.pem"

# Windows (PowerShell)
$env:ALOHOMORA_PRIVATE_KEY = "C:\keys\private.pem"
$env:ALOHOMORA_PUBLIC_KEY  = "C:\keys\public.pem"
```

If the variables are **not set**, Alohomora falls back to `.KEYS/PRIVATE_KEY.pem` and `.KEYS/PUBLIC_KEY.pem` in the current directory.

---

## Crash safety (.bak backups)

Before touching any file, Alohomora copies it to `<filename>.bak`.  
Once encryption/decryption succeeds the `.bak` is removed.

If a crash leaves `.bak` files behind, Alohomora will **refuse to run** on that path and show you the stale backups so you can inspect them first.

---

## Security notes

- Uses RSA-OAEP with SHA-256 (via the `cryptography` library).
- **Delete your private key** after encrypting if you want to lock files permanently.
- Store your private key somewhere safe — without it, encrypted files cannot be recovered.