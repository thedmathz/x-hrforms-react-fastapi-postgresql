import hashlib
import base64

from cryptography.fernet import Fernet
from app.core.config import settings

fernet = Fernet(base64.urlsafe_b64encode(hashlib.sha256(settings.SECRET_KEY.encode()).digest()))

def fernet_encrypt(string): 
    return fernet.encrypt(string.encode())

def fernet_decrypt(hash): 
    return fernet.decrypt(hash).decode() 