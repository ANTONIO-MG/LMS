from django.contrib import admin

# Register your models here.
from .models import Notification, Message, Post

class NotificationAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('title', 'notification_group', 'updated_at')
    # filter the list view by given fields
    list_filter = ('user', 'notification_group')
    # search the list view by given fields
    search_fields = ('user', 'title')
    # show the number of items per page
    list_per_page = 20

class MessageAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('sender', 'recipient')
    # filter the list view by given fields
    list_filter = ('sender', 'recipient')
    # search the list view by given fields
    search_fields = ('sender', 'recipient')
    # show the number of items per page
    list_per_page = 20

class PostAdmin(admin.ModelAdmin):
    # show the list 
    list_display = ('user', 'title', 'notification_group')
    # filter the list view by given fields
    list_filter = ('user', 'title', 'notification_group')
    # search the list view by given fields
    search_fields = ('user', 'title', 'notification_group')
    # show the fields that are not editable
    list_per_page = 20

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Post, PostAdmin)

