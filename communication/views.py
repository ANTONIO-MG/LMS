"""" 
Function based vies for the base app, the base app is the application running all
User, Tasks, Notifications, Messages, Classrooms, Subjects CRUD (create, read, update, Delete) functions
This also manages the database sessions and data management
"""

# the imports
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import MessageForm, NotificationForm, PostForm
from usertasks.forms import TodoForm
from .models import Notification, Message
from allauth.account.views import SignupView
from users_auth.models import Person
from communication.models import Post


@login_required
def Conference(request):
    me = Person.objects.get(user=request.user)
    
    context = {'me': me.first_name + " " + me.last_name}
    return render(request, 'conference.html', context)


@login_required
def SendMessage(request):
    create = True
    form = MessageForm
    me = Person.objects.get(user=request.user)
    form.user =  me
    if request.method == "POST":
        form = MessageForm(request.POST)
        if  form.is_valid():
            new = form.save(commit=False)
            new.user = me
            return redirect('home')
    
    context = {'form': form, 'create': create}
    return render(request, 'message_form.html', context)


@login_required
def EditMessage(request, pk):
    
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
    message = Message.objects.get(id=pk)
    me = Person.objects.get(user=request.user)
    
    if me != message.user:
        return HttpResponse("Not Allowed to delete")
    
    if request.method == "POST":
        message.delete()
        return redirect('subject', pk=message.subject.id)

    return render(request, 'delete_message.html', {'obj': message})


@login_required
def SendNotification(request):
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
    create = False
    note = get_object_or_404(Notification, id=pk)
    me = Person.objects.get(user=request.user)

    if request.method == "POST":
        form = NotificationForm(request.POST, instance=note)
        if form.is_valid():
            # Delete the existing post
            note.delete()

            # Save the updated post
            form.instance.user = me
            new_instance = form.save()

            return redirect('home')
    else:
        form = NotificationForm(instance=note)

    context = {'form': form, 'create': create}
    return render(request, 'notification_form.html', context)


@login_required
def DeleteNotification(request, pk):
    notification = Notification.objects.get(id=pk)
    if request.method == "POST":
        notification.delete()
        return redirect('home')

    return render(request, 'delete_notification.html', {'obj': notification})

def MyNotification(request, pk):
    notification = Notification.objects.get(id=pk)
    context = {'notification': notification}
    return render(request, 'notification.html', context)

def MyNotifications(request):

    me = Person.objects.get(id=request.user.pk)
    notifications = Notification.objects.all()
    my_class = me.my_class
    context = {'notifications': notifications, 'my_class': my_class}
    return render(request, 'notifications_tab.html', context)


@login_required
def MyNotice(request, pk):
    # create an instance of the of the specific notification ou want to show using the pk
    notification = Notification.objects.get(id=pk)
    # pass the context to be rendered on the page
    context = {"notification": notification}
    return render(request, 'notice.html', context)

@login_required
def CreatePost(request):
    
    create = True
    me = Person.objects.get(user=request.user)
    form = PostForm(request.POST)

    if request.method == 'POST':
        new_post = Post.objects.create(
            user = me,
            title = request.POST.get('title'),
            post_body = request.POST.get('post'),
            picture = request.POST.get('post_picture'),
            media = request.POST.get('post_media'),
            
        )
        return redirect('home')
    context = {'form': form, 'create': create}

    return render(request, 'post_form.html', context)


@login_required
def EditPost(request, pk):
    
    create = False
    # Get the original task
    original_post = Post.objects.get(id=pk)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=original_post)
        if form.is_valid():
            # Delete the original post
            original_post.delete()

            # Create a new task with updated information
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
    post = Post.objects.get(id=pk)
    if request.method == "POST":
        post.delete()
        return redirect('home')

    return render(request, 'delete_post.html', {'obj': post})


@login_required
def AllPosts(request):
    all_posts = Post.objects.all()

    context = {'all_posts': all_posts}
    return render(request, 'all_posts.html', context)


@login_required
def MyPost(request, pk):
    post = Post.objects.get(id=pk)

    return render(request, 'delete_task.html', {'obj': post})

@login_required
def About(request):

    return render(request, 'about.html')

@login_required
def ContctUs(request):

    return render(request, 'contact.html')

@login_required
def Finance(request):

    return render(request, 'finance.html')

@login_required
def Store(request):

    return render(request, 'store.html')
