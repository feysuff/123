# audit_log/utils.py
from cryptography.fernet import Fernet
from django.conf import settings

def decrypt_log(encrypted_message: str) -> str:
    ENCRYPTION_KEY = getattr(settings, "LOG_ENCRYPTION_KEY", None)
    if not ENCRYPTION_KEY:
        raise ValueError("LOG_ENCRYPTION_KEY is not set in settings")
    fernet = Fernet(ENCRYPTION_KEY)
    return fernet.decrypt(encrypted_message.encode()).decode()
