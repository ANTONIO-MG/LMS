"""" 
User_auth URL's
"""

# imports the path function to be able to load static documents on the given OS path
from django.urls import include, path
from . import views


urlpatterns = [
    
    
    # # Here are the classroom URL's
    # path('class/<str:pk>', views.MyClass, name="class"),
    # path('create_classroom/', views.CreateClassroom, name="create_classroom"),
    # path('update_classroom/<str:pk>/', views.UpdateClassroom, name="update_classroom"),
    # path('delete_classroom/<str:pk>/', views.DeleteClassroom, name="delete_classroom"),
    
    # # Here are the message URL's
    # path('send_message/', views.SendMessage, name="send_message"),
    # path('edit_message/<str:pk>/', views.EditMessage, name="edit_message"),
    # path('delete_message/<str:pk>/', views.DeleteMessage, name="delete_message"),
    
    # # Here are the notifications URL's
    # path('send_notification/', views.SendNotification, name="send_notification"),
    # path('edit_notification/<str:pk>/', views.EditNotification, name="edit_notification"),
    # path('delete_notification/<str:pk>/', views.DeleteNotification, name="delete_notification"),
    # path('notice/<str:pk>', views.MyNotice, name="notice"),
    # path('notification/<str:pk>', views.MyNotification, name="notification"),
    
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