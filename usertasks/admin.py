from django.contrib import admin

# Register your models here.
from .models import TaskCompletion, TODO, Post

class TaskCompletionAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('user', 'task', 'score')
    # filter the list view by given fields
    list_filter = ('is_done', 'score')
    # search the list view by given fields
    search_fields = ('user', 'task')
    # show the fields that are not editable
    readonly_fields = ('created_at', 'updated_at', 'user', 'score')
    # show the number of items per page
    list_per_page = 20

class TODOAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('user', 'title', 'subject', 'task_date')
    # filter the list view by given fields
    list_filter = ('subject', 'task_date')
    # search the list view by given fields
    search_fields = ('title', 'subject', 'task_date', 'user')
    # show the fields that are not editable
    readonly_fields = ('created_at', 'updated_at', 'description', 'user')
    # show the number of items per page
    list_per_page = 20

class PostAdmin(admin.ModelAdmin):
    # show the list 
    list_display = ('user', 'title', 'created_at')
    # filter the list view by given fields
    list_filter = ('user', 'title', 'created_at')
    # search the list view by given fields
    search_fields = ('user', 'title', 'created_at', 'post_body')
    # show the fields that are not editable
    readonly_fields = ('user',)
     # show the number of items per page
    list_per_page = 20

admin.site.register(TaskCompletion, TaskCompletionAdmin)
admin.site.register(TODO, TODOAdmin)
admin.site.register(Post, PostAdmin)