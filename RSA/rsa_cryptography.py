import os, base64, sys, time
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
sys.path.append("./")
from colors import *

class RSA:
    def __init__(self):
        self.MAX_BYTES = 446
        self.MAX_CIPHER_LENGTH = 512
        self.PUBLIC_KEY = None
        self.PRIVATE_KEY = None

    def load_keys_from_file(self):

        PRIVATE_KEY_FILE = ".KEYS/PRIVATE_KEY.pem"
        PUBLIC_KEY_FILE  = ".KEYS/PUBLIC_KEY.pem"

        try:
            with open(PRIVATE_KEY_FILE, "rb") as key_file:
                self.PRIVATE_KEY = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )

            with open(PUBLIC_KEY_FILE, "rb") as key_file:
                self.PUBLIC_KEY = serialization.load_pem_public_key(
                    key_file.read(),
                    backend=default_backend()
                )

        except:
            self.PRIVATE_KEY = None
            self.PUBLIC_KEY = None

            print(BOLD+RED+"\n  💀 Key files not found OR Invalid Keys 💀"+END)
            print(BOLD+"\n  ⏳ Generating Keys with 4096 bits ...\n")
            self.generate_keys(4096)
            print(GREEN +BOLD+ "  ✅ Keys generated successfully\n")


    def generate_keys(self, bits):

        PRIVATE_KEY = rsa.generate_private_key(
        public_exponent=65537,
        key_size=bits,
        backend=default_backend()
        )
        PUBLIC_KEY = PRIVATE_KEY.public_key()

        PRIVATE_PEM = PRIVATE_KEY.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        PUBLIC_PEM = PUBLIC_KEY.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        with open('.KEYS/PRIVATE_KEY.pem', 'wb') as f:
            f.write(PRIVATE_PEM)
        with open('.KEYS/PUBLIC_KEY.pem', 'wb') as f:
            f.write(PUBLIC_PEM)

        self.PUBLIC_KEY = PUBLIC_KEY
        self.PRIVATE_KEY = PRIVATE_KEY

    def encrypt(self, MESSAGE):

        return self.PUBLIC_KEY.encrypt(
        MESSAGE,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
            )
        )

    def decrypt(self, CIPHER):
        return self.PRIVATE_KEY.decrypt(
        CIPHER,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        ))

    def _print_keys(self):
        print(self.PRIVATE_KEY)
        print(self.PUBLIC_KEY)

if __name__ == "__main__":
    RSA = RSA()
    RSA.generate_keys(4096)
    RSA.load_keys_from_file()
    RSA._print_keys()