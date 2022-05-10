from django.contrib import admin
from .models import *


@admin.register(Url)
class UrlsAdmin(admin.ModelAdmin):
    list_display = ['owner', 'full_url', 'hash_url', 'clicks', 'created_at']
