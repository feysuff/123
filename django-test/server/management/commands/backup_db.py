# server/management/commands/backup_db.py
import os
import hashlib
import shutil
from django.core.management.base import BaseCommand
from django.conf import settings
from datetime import datetime

class Command(BaseCommand):
    help = "Backup database with checksum"

    def handle(self, *args, **options):
        db_path = settings.DATABASES['default']['NAME']  # путь к sqlite/db
        backup_dir = os.path.join(settings.BASE_DIR, 'backups')
        os.makedirs(backup_dir, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        backup_file = os.path.join(backup_dir, f"db_backup_{timestamp}.sqlite3")

        shutil.copy2(db_path, backup_file)

        # Чексумма SHA256
        sha256_hash = hashlib.sha256()
        with open(backup_file, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        checksum = sha256_hash.hexdigest()

        self.stdout.write(self.style.SUCCESS(f"Backup created: {backup_file}"))
        self.stdout.write(self.style.SUCCESS(f"SHA256 checksum: {checksum}"))
