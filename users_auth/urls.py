"""" 
User_auth URL's
"""

# Import the path function to define URL patterns
from django.urls import include, path
from .views import *
from usertasks.views import MyTasks, ToDo, MyTask, CreateTask, EditTask, DeleteTask, CalenderView
from communication.views import (
    MyPost, SendMessage, EditMessage, DeleteMessage, MyNotifications, SendNotification, 
    DeleteNotification, EditNotification, MyNotification, EditPost, CreatePost, 
    DeletePost, MyNotice, AllPosts, About, ContctUs, Store, Finance, Conference
)

urlpatterns = [
    # Basic user URL patterns
    path('home/', Home, name="home"),  # Home page
    path('todo', ToDo, name="todo"),  # To-do list page
    path('about', About, name="about"),  # About page
    path('Contact_us', ContctUs, name="contact"),  # Contact us page
    path('store', Store, name="store"),  # Store page
    path('finance', Finance, name="finance"),  # Finance page

    # Landing Page
    path('', landing_page_view, name='landing_page'),  # Landing page

    # Reminders
    path('delete_reminder/<int:reminder_id>/', delete_reminder, name='delete_reminder'),  # Delete reminder

    # Classroom URL patterns
    path('class/<str:pk>', MyClass, name="class"),  # View a specific class

    # Chat view
    path('chat/<str:pk>', Chat_View, name="chat_view"),  # Chat view

    # Message URL patterns
    path('send_message/', SendMessage, name="send_message"),  # Send a message
    path('edit_message/<str:pk>/', EditMessage, name="edit_message"),  # Edit a message
    path('delete_message/<str:pk>/', DeleteMessage, name="delete_message"),  # Delete a message

    # Notification URL patterns
    path('send_notification/', SendNotification, name="send_notification"),  # Send a notification
    path('edit_notification/<str:pk>/', EditNotification, name="edit_notification"),  # Edit a notification
    path('delete_notification/<str:pk>/', DeleteNotification, name="delete_notification"),  # Delete a notification
    path('notice/<str:pk>', MyNotice, name="notice"),  # View a specific notice
    path('notification/<str:pk>', MyNotification, name="notification"),  # View a specific notification
    path('my_notifications', MyNotifications, name="my_notifications"),  # View all notifications

    # Task URL patterns
    path('create_task/', CreateTask, name="create_task"),  # Create a task
    path('edit_task/<str:pk>/', EditTask, name="edit_task"),  # Edit a task
    path('delete_task/<str:pk>/', DeleteTask, name="delete_task"),  # Delete a task
    path('task/<str:pk>', MyTask, name="task"),  # View a specific task
    path('my_tasks', MyTasks, name="my_tasks"),  # View all tasks

    # Profile URL patterns
    path('subject/<str:pk>', MySubject, name="subject"),  # View a specific subject
    path('profile/<str:pk>', Profile, name="profile"),  # View a specific profile
    path('edit_profile/<str:pk>', EditProfile, name="edit_profile"),  # Edit a profile

    # Post URL patterns
    path('post/<str:pk>', MyPost, name="post"),  # View a specific post
    path('all_posts', AllPosts, name="all_posts"),  # View all posts
    path('create_post', CreatePost, name="create_post"),  # Create a post
    path('edit_post/<str:pk>', EditPost, name="edit_post"),  # Edit a post
    path('delete_post/<str:pk>', DeletePost, name="delete_post"),  # Delete a post

    # Calendar view
    path('calender', CalenderView, name="calender"),  # Calendar view

    # Conference call URL
    path('conference', Conference, name="conference"),  # Conference call view
]