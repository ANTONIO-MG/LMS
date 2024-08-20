from django.contrib import admin

# Register your models here.
from .models import TaskCompletion, TODO, TimelineItem

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

class TimelineItemAdmin(admin.ModelAdmin):
    # show the list 
    list_display = ('title', 'category', 'created_at')
    # filter the list view by given fields
    list_filter = ('title', 'category', 'created_at')
    # search the list view by given fields
    search_fields = ('title', 'category', 'created_at')
    # show the fields that are not editable
    readonly_fields = ()
     # show the number of items per page
    list_per_page = 20


admin.site.register(TODO, TODOAdmin)
admin.site.register(TaskCompletion, TaskCompletionAdmin)
admin.site.register(TimelineItem, TimelineItemAdmin)