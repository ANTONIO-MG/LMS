from django.contrib import admin

# Register your models here.
from .models import TaskCompletion, TODO, Post

class TODOAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('title', 'subject', 'start_date', 'end_date')
    # filter the list view by given fields
    list_filter = ('subject', 'title')
    # search the list view by given fields
    search_fields = ('title', 'subject')
    # show the fields that are not editable
    readonly_fields = ('created_at', 'updated_at')
    # show the number of items per page
    list_per_page = 20

class TaskCompletionAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('task', 'score', 'end_date')
    # search the list view by given fields
    search_fields = ('user', 'task')
    # show the fields that are not editable
    readonly_fields = ('created_at', 'updated_at')
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


admin.site.register(TODO, TODOAdmin)
admin.site.register(TaskCompletion, TaskCompletionAdmin)
admin.site.register(Post, PostAdmin)