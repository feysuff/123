import os
import hashlib
import time
from pathlib import Path
from django.core.management.base import BaseCommand

# Список файлов для мониторинга
FILES_TO_CHECK = [
    "server/settings.py",
    ".env",
]

# Словарь для хранения прошлых хешей
previous_hashes = {}

class Command(BaseCommand):
    help = "Проверка целостности файлов в реальном времени"

    def calculate_file_hash(self, filepath):
        if not os.path.exists(filepath):
            return None
        sha = hashlib.sha256()
        with open(filepath, "rb") as f:
            while chunk := f.read(8192):
                sha.update(chunk)
        return sha.hexdigest()

    def handle(self, *args, **options):
        self.stdout.write("=== Запуск живой проверки целостности файлов ===\n(CTRL+C для выхода)")
        
        # Инициализация хешей
        for file_path in FILES_TO_CHECK:
            previous_hashes[file_path] = self.calculate_file_hash(file_path)

        try:
            while True:
                for file_path in FILES_TO_CHECK:
                    current_hash = self.calculate_file_hash(file_path)
                    prev_hash = previous_hashes.get(file_path)

                    if current_hash is None:
                        self.stdout.write(f"[ERROR] Файл не найден: {file_path}")
                    elif prev_hash != current_hash:
                        self.stdout.write(f"[CHANGED] Файл изменён: {file_path}")
                        previous_hashes[file_path] = current_hash
                time.sleep(1)  # пауза 1 секунда
        except KeyboardInterrupt:
            self.stdout.write("\n=== Мониторинг остановлен пользователем ===")
