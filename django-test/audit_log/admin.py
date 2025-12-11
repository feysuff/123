# audit_log/admin.py
from django.contrib import admin
from .models import LogEntry
from .utils import decrypt_log
from django.utils.html import format_html

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'level', 'logger', 'get_message')

    def get_message(self, obj):
        return format_html("<pre>{}</pre>", decrypt_log(obj.message))
    get_message.short_description = "Message"