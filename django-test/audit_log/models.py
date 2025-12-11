from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class LogEntry(models.Model):
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    level = models.CharField(max_length=10)
    logger = models.CharField(max_length=200)
    message = models.TextField()  # здесь будет храниться зашифрованный текст
    user = models.ForeignKey(
        User,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="auditlog_entries"
    )
    ip = models.GenericIPAddressField(null=True, blank=True)
    path = models.CharField(max_length=500, null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} | {self.level} | {self.logger}"
