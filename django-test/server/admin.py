# server/admin.py
from django.contrib import admin
from .models import Order
from django.urls import path
from django.http import HttpResponse
import hashlib, os
from django.conf import settings
from django.utils.html import format_html


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product_name', 'quantity', 'total_price', 'created_at')
    readonly_fields = ('created_at',)



class OrderAdmin(admin.ModelAdmin):

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('download-db/', self.admin_site.admin_view(self.download_db), name='download-db'),
        ]
        return custom_urls + urls

    def download_db(self, request):
        db_path = settings.DATABASES['default']['NAME']
        with open(db_path, 'rb') as f:
            data = f.read()
        checksum = hashlib.sha256(data).hexdigest()

        response = HttpResponse(data, content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(db_path)}"'
        response['X-Checksum-SHA256'] = checksum
        return response
