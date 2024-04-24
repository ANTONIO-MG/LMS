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
from .forms import ClassRoomForm, MessageForm, NotificationForm, TodoForm, PostForm, PersonForm, PersonEditForm, EditProfileForm
from .models import Classroom, Notification, TODO, Message, Subject, TaskCompletion, Post, Person
from allauth.account.views import SignupView

@login_required
def SendMessage(request):
    create = True
    form = MessageForm
    form.user =  request.user
    if request.method == "POST":
        form = MessageForm(request.POST)
        if  form.is_valid():
            new = form.save(commit=False)
            new.user = request.user
            return redirect('home')
    
    context = {'form': form, 'create': create}
    return render(request, 'message_form.html', context)


@login_required
def EditMessage(request, pk):
    
    create = False
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
    
    if request.user != message.user:
        return HttpResponse("Not Allowed to delete")
    
    if request.method == "POST":
        message.delete()
        return redirect('subject', pk=message.subject.id)

    return render(request, 'delete_message.html', {'obj': message})


@login_required
def SendNotification(request):
    form = NotificationForm
    if request.method == "POST":
        form = NotificationForm(request.POST)
        
        if form.is_valid():
            form.instance.user = request.user
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'notification_form.html', context)

@login_required
def EditNotification(request, pk):
    create = False
    note = get_object_or_404(Notification, id=pk)

    if request.method == "POST":
        form = NotificationForm(request.POST, instance=note)
        if form.is_valid():
            # Delete the existing post
            note.delete()

            # Save the updated post
            form.instance.user = request.user
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


@login_required
def MyNotice(request, pk):
    # create an instance of the of the specific notification ou want to show using the pk
    notification = Notification.objects.get(id=pk)
    # pass the context to be rendered on the page
    context = {"notification": notification}
    return render(request, 'notice.html', context)

