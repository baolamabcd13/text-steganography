import hashlib
import base64
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class Encryptor:
    def __init__(self):
        self.salt = b'steganography_salt'  # Salt cố định cho PBKDF2
    
    def generate_key(self, password):
        """Tạo khóa mã hóa từ mật khẩu"""
        password_bytes = password.encode('utf-8')
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password_bytes))
        return key
    
    def encrypt(self, message, password):
        """Mã hóa thông điệp với mật khẩu"""
        if not message or not password:
            return ""
        
        key = self.generate_key(password)
        f = Fernet(key)
        encrypted_message = f.encrypt(message.encode('utf-8'))
        return base64.urlsafe_b64encode(encrypted_message).decode('utf-8')
    
    def decrypt(self, encrypted_message, password):
        """Giải mã thông điệp với mật khẩu"""
        if not encrypted_message or not password:
            return ""
        
        try:
            key = self.generate_key(password)
            f = Fernet(key)
            decoded = base64.urlsafe_b64decode(encrypted_message.encode('utf-8'))
            decrypted_message = f.decrypt(decoded)
            return decrypted_message.decode('utf-8')
        except Exception as e:
            raise ValueError("Mật khẩu không đúng hoặc thông điệp bị hỏng")