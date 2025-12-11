# clear_logs.py
import os
import django

# Настройки проекта
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "server.settings")
django.setup()  # инициализация Django

from audit_log.models import LogEntry

def clear_all_logs():
    count, _ = LogEntry.objects.all().delete()
    print(f"Удалено {count} записей из журнала.")

if __name__ == "__main__":
    clear_all_logs()
