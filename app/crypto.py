from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import os

class CryptoManager:
    def __init__(self, master_password, salt=None):
        self.master_password = master_password.encode()
        self.salt = salt if salt else os.urandom(16)
        self._setup_encryption()

    def _setup_encryption(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt if isinstance(self.salt, bytes) else base64.b64decode(self.salt),
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_password))
        self.fernet = Fernet(key)

    def encrypt(self, data):
        return self.fernet.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        return self.fernet.decrypt(encrypted_data.encode()).decode()

    def get_salt(self):
        if isinstance(self.salt, bytes):
            return base64.b64encode(self.salt).decode()
        return self.salt 