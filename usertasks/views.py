"""" 
Function based vies for the base app, the base app is the application running all
User, Tasks, Notifications, Messages, Classrooms, Subjects CRUD (create, read, update, Delete) functions
This also manages the database sessions and data management
"""

# the imports
import json
from django.utils import timezone
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .forms import TodoForm
from .models import TODO, TaskCompletion, Person, Reminder


def ToDo(request):
    todo = TODO.objects.all()
    context = {"todo": todo}
    return render(request, 'home.html', context)


def MyTasks(request):

    me = Person.objects.get(id=request.user.pk)
    tasks = TODO.objects.all()
    personal_tasks = TaskCompletion.objects.all()
    my_class = me.my_class
    assigned_task = TaskCompletion.objects.filter(user=me)
    context = {'tasks': tasks, 'personal_tasks': personal_tasks,
               'me': me, 'my_class': my_class, 'assigned_task': assigned_task}
    return render(request, 'tasks_list.html', context)


@login_required
def MyTask(request, pk):
    # create an instance of the of the specific notification ou want to show using the pk
    tasks = TaskCompletion.objects.get(id=pk)
    subject_task = TODO.objects.get(title=tasks.task)
    # pass the context to be rendered on the page
    context = {"tasks": tasks, 'subject_task': subject_task}
    return render(request, 'todo.html', context)


@login_required
def CreateTask(request):
    create = True
    me = Person.objects.get(user=request.user)
    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            # Save the task, but don't commit to the database yet
            task = form.save(commit=False)

            # Assign the current logged-in user to the task's user field
            task.user = me

            # Now save the task with the user field populated
            task.save()

            # Automatically add the task to all participants in the selected subject(s)
            print("completed the todo")
            selected_subject = form.cleaned_data['subject']
            participants = selected_subject.participants.all()
            print(participants)

            for participant in participants:
                # Create TaskCompletion for each participant
                print("started to assign teh taskcompletion")
                TaskCompletion.objects.create(
                    user=participant,
                    task=task,
                    start_date = task.start_date,
                    end_date = task.end_date,
                )
                print("Completed to assign the taskcompletion")
            return redirect('home')
    else:
        form = TodoForm()

    context = {'form': form, 'create': create}
    return render(request, 'todo_form.html', context)


@login_required
def EditTask(request, pk):
    create = False
    # Get the original task
    original_task = TODO.objects.get(id=pk)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=original_task)
        if form.is_valid():
            # Delete the original task
            original_task.delete()

            # Create a new task with updated information
            new_task = form.save(commit=False)
            new_task.created_at = original_task.created_at  # Keep the original creation date
            new_task.updated_at = timezone.now()  # Update the updated date to now
            new_task.save()

            return redirect('home')
    else:
        form = TodoForm(instance=original_task)

    context = {'form': form, 'create': create}
    return render(request, 'todo_form.html', context)


@login_required
def DeleteTask(request, pk):
    tasks = TODO.objects.get(id=pk)
    if request.method == "POST":
        tasks.delete()
        return redirect('home')

    return render(request, 'delete_task.html', {'obj': tasks})

@login_required
def CalenderView(request):
    # Fetch ToDo items from the database
    todos = TODO.objects.all()

    # Create a list of events from ToDo items
    todo_events = [
        {
            'title': todo.title,
            'start': todo.created_at.isoformat(),  # Assuming `created_at` is the timestamp of the ToDo
            'backgroundColor': '#3c8dbc',  # You can customize the color
            'borderColor': '#3c8dbc',
            'allDay': True,
        }
        for todo in todos
    ]

    context = {
        'todo_events': todo_events,
    }
    return render(request, 'calendar.html', context)
