import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


# OAEP with SHA-256 overhead = 2 + 2*32 = 66 bytes
# So max plaintext per block = key_size_bytes - 66
_OAEP_OVERHEAD = 66


class RSAError(Exception):
    """Raised for any RSA key / crypto failure."""
    pass


class RSA:
    def __init__(self):
        self.PUBLIC_KEY  = None
        self.PRIVATE_KEY = None
        self._key_size_bytes = 512   # default (4096-bit key)

    # ------------------------------------------------------------------
    # Properties derived from actual key size
    # ------------------------------------------------------------------
    @property
    def MAX_BYTES(self) -> int:
        """Maximum plaintext bytes per encrypt call."""
        return self._key_size_bytes - _OAEP_OVERHEAD

    @property
    def MAX_CIPHER_LENGTH(self) -> int:
        """Ciphertext block size (equals key size in bytes)."""
        return self._key_size_bytes

    # ------------------------------------------------------------------
    # Key loading
    # ------------------------------------------------------------------
    def load_keys_from_file(self) -> str:
        """
        Try env vars first, then fall back to .KEYS/ directory.
        Returns a string describing the source that was used.
        Raises RSAError on any failure.
        """
        env_priv = os.environ.get("ALOHOMORA_PRIVATE_KEY")
        env_pub  = os.environ.get("ALOHOMORA_PUBLIC_KEY")

        if env_priv and env_pub:
            self._load_pem_paths(env_priv, env_pub)
            return "environment variables"
        else:
            fallback_priv = os.path.join(".KEYS", "PRIVATE_KEY.pem")
            fallback_pub  = os.path.join(".KEYS", "PUBLIC_KEY.pem")
            self._load_pem_paths(fallback_priv, fallback_pub)
            return ".KEYS directory"

    def _load_pem_paths(self, private_path: str, public_path: str):
        """Load key pair from two PEM file paths. Raises RSAError on any problem."""
        for path, label in ((private_path, "private"), (public_path, "public")):
            if not os.path.isfile(path):
                raise RSAError(f"Key file not found ({label}): {path}")

        try:
            with open(private_path, "rb") as f:
                self.PRIVATE_KEY = serialization.load_pem_private_key(
                    f.read(), password=None, backend=default_backend()
                )
        except Exception as exc:
            raise RSAError(f"Failed to load private key: {exc}") from exc

        try:
            with open(public_path, "rb") as f:
                self.PUBLIC_KEY = serialization.load_pem_public_key(
                    f.read(), backend=default_backend()
                )
        except Exception as exc:
            raise RSAError(f"Failed to load public key: {exc}") from exc

        self._update_key_size()

    def _update_key_size(self):
        """Cache the key size in bytes from the loaded private key."""
        if self.PRIVATE_KEY is not None:
            self._key_size_bytes = self.PRIVATE_KEY.key_size // 8

    # ------------------------------------------------------------------
    # Key generation
    # ------------------------------------------------------------------
    def generate_keys(self, bits: int):
        """Generate a new RSA key pair and write to .KEYS/."""
        if bits < 530 or bits > 4096:
            raise RSAError(f"Key size {bits} is out of allowed range [530, 4096].")

        os.makedirs(".KEYS", exist_ok=True)

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=bits,
            backend=default_backend(),
        )
        public_key = private_key.public_key()

        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )

        with open(".KEYS/PRIVATE_KEY.pem", "wb") as f:
            f.write(private_pem)
        with open(".KEYS/PUBLIC_KEY.pem", "wb") as f:
            f.write(public_pem)

        self.PRIVATE_KEY = private_key
        self.PUBLIC_KEY  = public_key
        self._key_size_bytes = bits // 8

    # ------------------------------------------------------------------
    # Crypto primitives
    # ------------------------------------------------------------------
    def encrypt(self, message: bytes) -> bytes:
        if self.PUBLIC_KEY is None:
            raise RSAError("No public key loaded.")
        return self.PUBLIC_KEY.encrypt(
            message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    def decrypt(self, cipher: bytes) -> bytes:
        if self.PRIVATE_KEY is None:
            raise RSAError("No private key loaded.")
        return self.PRIVATE_KEY.decrypt(
            cipher,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

    def keys_loaded(self) -> bool:
        return self.PUBLIC_KEY is not None and self.PRIVATE_KEY is not None

    def _print_keys(self):
        print(self.PRIVATE_KEY)
        print(self.PUBLIC_KEY)


# ------------------------------------------------------------------
# Quick smoke-test
# ------------------------------------------------------------------
if __name__ == "__main__":
    r = RSA()
    r.generate_keys(2048)
    r.load_keys_from_file()
    msg = b"Hello Alohomora!"
    assert r.decrypt(r.encrypt(msg)) == msg
    print("RSA smoke-test passed.")