# Alohomora - Hide Secrets using RSA

Alohomora is a Python project that provides encryption and decryption functionality for files and directories using user-generated RSA key pairs. It ensures high security by utilizing 4096-bit encryption.

## Keywords

Encrypt file, Encrypt directory, Decrypt file, Decrypt directory, RSA encryption, RSA decryption, RSA file encryption

## Installation

To use Alohomora, you need to have the `cryptography` module installed. If you don't have it, you can install it by running any of the following command:

```bash
pip install cryptography
pip3 install cryptography
```

## Getting started

If you already have RSA key pairs, then paste it into the `.KEYS/` directory with `Private Key` file named of `PRIVATE_KEY.pem` and `Public Key` file named of `PUBLIC_KEY.pem`.

If you don't have RSA Key pairs, then you can generate RSA key pairs from main menu. Please do only use `4096` bits as it works perfectly fine.

To run <b>Alohomora</b> file encryption/decryption tool, To get started, you can use any of the following commands:

```bash
python3 alohomora.py
py alohomora.py
python alohomora.py
```

## Caution
After encryption/decryption, please destroy your both key files in `.KEYS/` directory so no one can access your secrets! 

## Features
1. Generate RSA key pairs
2. Load Keys from .KEYS/ directory
3. Encrypt file or directory
4. Decrypt file or directory

## Contribution

Contributions to Alohomora are welcome! If you would like to contribute, please follow these steps:

1. Fork the repository
2. Create a new branch for your feature or bug fix
3. Develop and test your changes
4. Commit your changes and push them to your forked repository
5. Open a pull request to submit your contribution
