from django.contrib import admin

# Register your models here.
from .models import Notification, Message

class NotificationAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('user', 'class_room', 'subject', 'created_at', 'updated_at')
    # filter the list view by given fields
    list_filter = ('user', 'class_room', 'subject')
    # search the list view by given fields
    search_fields = ('user', 'class_room', 'subject')
    # show the number of items per page
    list_per_page = 20

class MessageAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('user', 'title', 'created_at', 'updated_at')
    # filter the list view by given fields
    list_filter = ('user')
    # search the list view by given fields
    search_fields = ('user', 'title')
    # show the number of items per page
    list_per_page = 20

admin.site.register(Notification)
admin.site.register(Message)
