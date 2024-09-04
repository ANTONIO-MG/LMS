"""" 
Function-based views for the base app. The base app handles all CRUD (Create, Read, Update, Delete) operations for Users, Tasks, Notifications, Messages, Classrooms, and Subjects. It also manages database sessions and data management.
"""

# Imports
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from .forms import MessageForm, NotificationForm, PostForm
from usertasks.forms import TodoForm
from .models import Notification, Message, Post
from users_auth.models import Person
from django.db.models.signals import post_save
from django.dispatch import receiver

@login_required
def Conference(request):
    """
    View to render the conference page.
    """
    me = Person.objects.get(user=request.user)
    context = {'me': me.first_name + " " + me.last_name}
    return render(request, 'conference.html', context)

@login_required
def SendMessage(request):
    """
    View to handle sending a message.
    """
    create = True
    form = MessageForm
    me = Person.objects.get(user=request.user)
    form.user = me
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            new = form.save(commit=False)
            new.user = me
            return redirect('home')
    
    context = {'form': form, 'create': create}
    return render(request, 'message_form.html', context)

@login_required
def EditMessage(request, pk):
    """
    View to handle editing a message.
    """
    create = False
    me = Person.objects.get(user=request.user)
    message = get_object_or_404(Message, id=pk)
    form = Message.objects.get(id=pk)
    form = MessageForm(instance=form)
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            form.save()
            message.delete()
            return redirect('home')
    
    context = {'form': form, 'create': create}
    return render(request, 'message_form.html', context)

@login_required
def DeleteMessage(request, pk):
    """
    View to handle deleting a message.
    """
    message = Message.objects.get(id=pk)
    me = Person.objects.get(user=request.user)
    
    if request.method == "POST":
        message.delete()
        return redirect('subject', pk=message.subject.id)

    return render(request, 'delete_message.html', {'obj': message})

@login_required
def SendNotification(request):
    """
    View to handle sending a notification.
    """
    me = Person.objects.get(user=request.user)
    form = NotificationForm
    if request.method == "POST":
        form = NotificationForm(request.POST)
        
        if form.is_valid():
            form.instance.user = me
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'notification_form.html', context)

@login_required
def EditNotification(request, pk):
    """
    View to handle editing a notification.
    """
    create = False
    note = get_object_or_404(Notification, id=pk)
    me = Person.objects.get(user=request.user)

    if request.method == "POST":
        form = NotificationForm(request.POST, instance=note)
        if form.is_valid():
            # Delete the existing notification
            note.delete()

            # Save the updated notification
            form.instance.user = me
            new_instance = form.save()

            return redirect('home')
    else:
        form = NotificationForm(instance=note)

    context = {'form': form, 'create': create}
    return render(request, 'notification_form.html', context)

@login_required
def DeleteNotification(request, pk):
    """
    View to handle deleting a notification.
    """
    notification = Notification.objects.get(id=pk)
    if request.method == "POST":
        notification.delete()
        return redirect('home')

    return render(request, 'delete_notification.html', {'obj': notification})

def MyNotification(request, pk):
    """
    View to display a specific notification.
    """
    notification = Notification.objects.get(id=pk)
    context = {'notification': notification}
    return render(request, 'notification.html', context)

def MyNotifications(request):
    """
    View to display all notifications for the logged-in user.
    """
    me = Person.objects.get(id=request.user.pk)
    notifications = Notification.objects.all()
    my_class = me.my_class
    context = {'notifications': notifications, 'my_class': my_class}
    return render(request, 'notifications_tab.html', context)

@login_required
def MyNotice(request, pk):
    """
    View to display a specific notice.
    """
    notification = Notification.objects.get(id=pk)
    context = {"notification": notification}
    return render(request, 'notice.html', context)

@login_required
def CreatePost(request):
    """
    View to handle creating a new post.
    """
    create = True
    me = Person.objects.get(user=request.user)
    form = PostForm(request.POST)

    if request.method == 'POST':
        new_post = Post.objects.create(
            user=me,
            title=request.POST.get('title'),
            post_body=request.POST.get('post'),
            picture=request.POST.get('post_picture'),
            media=request.POST.get('post_media'),
        )
        return redirect('home')
    context = {'form': form, 'create': create}

    return render(request, 'post_form.html', context)

@login_required
def EditPost(request, pk):
    """
    View to handle editing a post.
    """
    create = False
    original_post = Post.objects.get(id=pk)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=original_post)
        if form.is_valid():
            # Delete the original post
            original_post.delete()

            # Create a new post with updated information
            new_post = form.save(commit=False)
            new_post.created_at = original_post.created_at  # Keep the original creation date
            new_post.updated_at = timezone.now()  # Update the updated date to now
            new_post.save()

            return redirect('home')
    else:
        form = PostForm(instance=original_post)

    context = {'form': form, 'create': create}
    return render(request, 'post_form.html', context)

@login_required
def DeletePost(request, pk):
    """
    View to handle deleting a post.
    """
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')

    return render(request, 'delete_post.html', {'obj': post})

@login_required
def AllPosts(request):
    """
    View to display all posts.
    """
    all_posts = Post.objects.all()
    context = {'all_posts': all_posts}
    return render(request, 'all_posts.html', context)

@login_required
def MyPost(request, pk):
    """
    View to display a specific post.
    """
    post = Post.objects.get(id=pk)
    return render(request, 'delete_task.html', {'obj': post})

@login_required
def About(request):
    """
    View to display the about page.
    """
    return render(request, 'about.html')

@login_required
def ContctUs(request):
    """
    View to display the contact us page.
    """
    return render(request, 'contact.html')