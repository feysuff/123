# audit_log/handlers.py
import logging
from cryptography.fernet import Fernet
from django.conf import settings

class EncryptedDBLogHandler(logging.Handler):
    def emit(self, record):
        try:
            from audit_log.models import LogEntry
            from django.contrib.auth import get_user_model
            User = get_user_model()

            # создаём Fernet здесь, внутри emit
            ENCRYPTION_KEY = getattr(settings, "LOG_ENCRYPTION_KEY", None)
            if not ENCRYPTION_KEY:
                ENCRYPTION_KEY = Fernet.generate_key()
            fernet = Fernet(ENCRYPTION_KEY)

            message = self.format(record).encode()
            encrypted = fernet.encrypt(message)

            user = getattr(record, "user", None)

            LogEntry.objects.create(
                level=record.levelname,
                logger=record.name,
                message=encrypted.decode(),
                user=user if user and user.is_authenticated else None,
                ip=getattr(record, "ip", None),
                path=getattr(record, "path", None),
                meta=getattr(record, "meta", {}),
            )
        except Exception:
            self.handleError(record)
