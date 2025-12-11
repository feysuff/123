# check_logs.py
import os
import django
import logging

# Настройки проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()  # инициализация Django

from audit_log.models import LogEntry
from audit_log.utils import decrypt_log

def create_test_log():
    logger = logging.getLogger("audit_log")
    logger.info("Тест шифрованного лога")

def show_logs():
    logs = LogEntry.objects.all()
    print(f"Всего логов: {logs.count()}\n")

    print("=== Зашифрованные логи ===")
    for i, entry in enumerate(logs, start=1):
        print(f"{i}. {entry.level} | {entry.path} | {entry.message}")

    print("\n=== Расшифрованные логи ===")
    for i, entry in enumerate(logs, start=1):
        try:
            decrypted = decrypt_log(entry.message)
        except Exception as e:
            decrypted = f"Ошибка расшифровки: {e}"
        print(f"{i}. {entry.level} | {entry.path} | {decrypted}")

if __name__ == "__main__":
    create_test_log()
    show_logs()
