from django.contrib import admin
from .models import Notification


class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'sender', 'receiver', 'notification_type', 'created_at']


admin.site.register(Notification, NotificationAdmin)
