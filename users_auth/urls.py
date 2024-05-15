"""" 
User_auth URL's
"""

# imports the path function to be able to load static documents on the given OS path
from django.urls import include, path
from .views import *
from usertasks.views import MyTasks, ToDo, MyTask, CreateTask, EditTask, DeleteTask
from communication.views import MyPost, SendMessage, EditMessage, DeleteMessage, MyNotifications, SendNotification, DeleteNotification, EditNotification, MyNotification, EditPost, CreatePost, DeletePost, MyNotice


urlpatterns = [
    
    #pattern for the all_users view
    #django allauth
    
    
    # this are the basic user URL's
    path('home/', Home, name="home"),
    path('register/', Register, name="register"),
    path('todo', ToDo, name="todo"),
    
    # Here are the classroom URL's
    path('class/<str:pk>', MyClass, name="class"),
    path('create_classroom/', CreateClassroom, name="create_classroom"),
    path('update_classroom/<str:pk>/', UpdateClassroom, name="update_classroom"),
    path('delete_classroom/<str:pk>/', DeleteClassroom, name="delete_classroom"),
    
    # # Here are the message URL's
    path('send_message/', SendMessage, name="send_message"),
    path('edit_message/<str:pk>/', EditMessage, name="edit_message"),
    path('delete_message/<str:pk>/', DeleteMessage, name="delete_message"),
    
    # # Here are the notifications URL's
    path('send_notification/', SendNotification, name="send_notification"),
    path('edit_notification/<str:pk>/', EditNotification, name="edit_notification"),
    path('delete_notification/<str:pk>/', DeleteNotification, name="delete_notification"),
    path('notice/<str:pk>', MyNotice, name="notice"),
    path('notification/<str:pk>', MyNotification, name="notification"),
    
    # # Here are the tasks URL's
    path('create_task/', CreateTask, name="create_task"),
    path('edit_task/<str:pk>/', EditTask, name="edit_task"),
    path('delete_task/<str:pk>/', DeleteTask, name="delete_task"),
    path('task/<str:pk>', MyTask, name="task"),
    
    # Here are the profile URL's
    path('subject/<str:pk>', MySubject, name="subject"),
    path('my_subjects', MySubjects, name="my_subjects"),
    path('profile/<str:pk>', Profile, name="profile"),
    path('edit_profile/<str:pk>', EditProfile, name="edit_profile"),
    
    # # Here are the posts URL's
    path('post/<str:pk>', MyPost, name="post"),
    path('create_post', CreatePost, name="create_post"),
    path('edit_post/<str:pk>', EditPost, name="edit_post"),
    path('delete_post/<str:pk>', DeletePost, name="delete_post"),
    
    # # view the list of notifications
    path('my_notifications', MyNotifications, name="my_notifications"),
    
    # tasks list
    path('my_tasks', MyTasks, name="my_tasks"),
    
    
] 