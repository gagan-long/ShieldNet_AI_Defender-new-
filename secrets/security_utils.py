# Example: AES-256 encryption for logs
from cryptography.fernet import Fernet

class SecurityUtil:
    def __init__(self):
        self.key = Fernet.generate_key()
        
    def encrypt_data(self, data: str) -> bytes:
        return Fernet(self.key).encrypt(data.encode())
        
    def decrypt_data(self, encrypted: bytes) -> str:
        return Fernet(self.key).decrypt(encrypted).decode()
