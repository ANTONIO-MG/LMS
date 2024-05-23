from django.contrib import admin

# Register your models here.
from .models import Person, Classroom, Subject

class PersonAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('first_name', 'last_name', 'email', 'contact_number')
    # filter the list view by given fields
    list_filter = ('email', 'first_name', 'last_name', 'user_type')
    # search the list view by given fields
    search_fields = ('first_name', 'Last_name', 'email', 'my_class', 'contact_number')
    # show the number of items per page
    list_per_page = 20

class ClassroomAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('name', 'teacher')
    # filter the list view by given fields
    list_filter = ('subjects', 'teacher')
    # search the list view by given fields
    search_fields = ('name', 'teacher', 'subjects')
    # show the number of items per page
    list_per_page = 20

class SubjectAdmin(admin.ModelAdmin):
    # show the list view on the admin panel
    list_display = ('title', 'teacher', 'class_room')
    # filter the list view by given fields
    list_filter = ('class_room', 'teacher')
    # search the list view by given fields
    search_fields = ('title', 'teacher', 'class_room')
    # show the number of items per page
    list_per_page = 20


admin.site.register(Person, PersonAdmin)
admin.site.register(Classroom, ClassroomAdmin)
admin.site.register(Subject, SubjectAdmin)