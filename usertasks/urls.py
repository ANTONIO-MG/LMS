"""" 
Tasks Url's
"""

# imports the path function to be able to load static documents on the given OS path
from django.urls import include, path
from . import views


urlpatterns = [
    
    #pattern for the all_users view
    #django allauth

    # # Here are the tasks URL's
    # path('create_task/', views.CreateTask, name="create_task"),
    # path('edit_task/<str:pk>/', views.EditTask, name="edit_task"),
    # path('delete_task/<str:pk>/', views.DeleteTask, name="delete_task"),
    # path('task/<str:pk>', views.MyTask, name="task"),
    
    # # Here are the profile URL's
    # path('subject/<str:pk>', views.MySubject, name="subject"),
    # path('profile/<str:pk>', views.Profile, name="profile"),
    # path('edit_profile/<str:pk>', views.EditProfile, name="edit_profile"),
    
    # # Here are the posts URL's
    # path('post/<str:pk>', views.MyPost, name="post"),
    # path('create_post', views.CreatePost, name="create_post"),
    # path('edit_post/<str:pk>', views.EditPost, name="edit_post"),
    # path('delete_post/<str:pk>', views.DeletePost, name="delete_post"),
    
    # # view the list of subjects
    # path('my_subjects', views.MySubjects, name="my_subjects"),
    
    # # view the list of notifications
    # path('my_notifications', views.MyNotifications, name="my_notifications"),
    
    # # tasks list
    # path('my_tasks', views.MyTasks, name="my_tasks"),
    
    
] 