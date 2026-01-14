from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

# argon 2 (for passwords)
ph = PasswordHasher()

def argon2_encrypt(string) -> str: 
    return ph.hash(string)  

def argon2_verify(hashed, password) -> bool: 
    try:
        return ph.verify(hashed, password)
    except VerifyMismatchError:
        return False
    except Exception:
        # Optional: handle other unexpected exceptions
        return False