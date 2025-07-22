# admin.py

from django.contrib import admin
from .models import ShareRecord


@admin.register(ShareRecord)
class ShareRecordAdmin(admin.ModelAdmin):
    list_display = ['share_id', 'project_name', 'status', 'member_id', 'received_transaction']
