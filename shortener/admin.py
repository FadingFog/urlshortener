from django.contrib import admin
from .models import *


@admin.register(Urls)
class UrlsAdmin(admin.ModelAdmin):
    list_display = ['full_url', 'hash_url', 'clicks', 'created_at']
