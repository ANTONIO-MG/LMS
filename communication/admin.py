from django.contrib import admin

# Register your models here.
from .models import Notification, Message, Post

class NotificationAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('title', 'notification_group', 'updated_at')
    # filter the list view by given fields
    list_filter = ('user', 'notification_group')
    # search the list view by given fields
    search_fields = ('user', 'notification_group')
    # show the number of items per page
    list_per_page = 20

class MessageAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('user', 'created_at', 'updated_at')
    # filter the list view by given fields
    list_filter = ('user', 'updated_at')
    # search the list view by given fields
    search_fields = ('user', 'title')
    # show the number of items per page
    list_per_page = 20

class PostAdmin(admin.ModelAdmin):
    # show the list 
    list_display = ('title', 'created_at', 'user')
    # filter the list view by given fields
    list_filter = ('user', 'title', 'created_at')
    # search the list view by given fields
    search_fields = ('user', 'title', 'created_at', 'post_body')
    # show the fields that are not editable
    readonly_fields = ()
     # show the number of items per page
    list_per_page = 20

admin.site.register(Notification, NotificationAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Post, PostAdmin)

