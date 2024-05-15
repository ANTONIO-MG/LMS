from datetime import timezone
from pyexpat.errors import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render

from communication.forms import ClassRoomForm
from .  forms import PersonForm, PersonEditForm
from usertasks.models import TaskCompletion, TODO
from communication.models import Notification, Message, Post
from users_auth.models import Classroom, Person, Subject

# Create your views here.

# The homepage view
def Home(request):
    """
    classroom: stores all the classroom as objects and can be queried
    messages: stores all the messages on teh database and can be queried
    """
    
    classrooms = Classroom.objects.all()
    messages = Message.objects.all()
    notifications = Notification.objects.all()[0:3]
    tasks = TODO.objects.all()
    all_users = Person.objects.all()
    assigned_task = TaskCompletion.objects.filter(user=request.user.id)
    subjects = Subject.objects.all()
    print(request.user)
    me = Person.objects.get(user=request.user.id)

    my_class = me.my_class

    context = {"classrooms": classrooms, "messages" : messages,
               "notifications" : notifications, "tasks": tasks,
               "subjects": subjects, 'my_class': my_class,
               'all_users': all_users, 'assigned_task': assigned_task}
    return  render(request, 'home.html', context)


def Profile(request):
    me = Person.objects.get(id=pk)
    all_posts = Post.objects.all()
    all_users = Person.objects.all()
    subjects = me.participants.all()
    classrooms = Classroom.objects.all()
    messages = Message.objects.all()
    notifications = Notification.objects.all()[0:5]
    my_class = request.user.my_class
    context = {"classrooms": classrooms, "messages": messages,
               "notifications": notifications, "tasks": tasks,
               'me':me, 'subjects': subjects,
               'all_users': all_users, 'all_posts': all_posts, 'my_class': my_class, }
    return render(request, 'profile.html')



def EditProfile(request, pk):
    person = Person.objects.get(id=pk)
    form = PersonEditForm(instance=person)
    if request.method == "POST":
        form = PersonEditForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'edit_profile.html', context)


def Register(request):
    form = PersonForm()
    if request.method == 'POST':
        print("passed the request method")
        form = PersonForm(request.POST)
        if form.is_valid():
            print("passed the form is valid")
            new_user = form.save(commit=False)
            new_user.user = request.user
            new_user.email = request.user.email
            new_user.save()
            print("passed the save method")

            # Assuming you have a field in your Person model to store the selected class
            selected_class = new_user.my_class

            # Add the new user as a participant to all the subjects of the selected class
            subjects_for_class = selected_class.subjects.all()
            for subject in subjects_for_class:
                subject.participants.add(new_user)

            # Add the new user as a participant to the participants of the selected class
            selected_class.participants.add(new_user)
            
            print("new user created: " + request.user.email)
            return redirect('home')
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, "register.html", context)


def MySubject(request, pk):
    subj = Subject.objects.get(id=pk)
    messages = Message.objects.all()
    people = Person.objects.all()
    person = Person.objects.get(id=request.user.id)
    participants = subj.participants.all()
    classroom = Classroom.objects.get(id=subj.room.id)  # Corrected line

    if request.method == 'POST':
        new_message = Message.objects.create(
            user=request.user,
            content=request.POST.get('message'),  # Corrected line
            subject=subj,
            class_room =subj.room
        )
        return redirect('subject', pk=subj.id)

    context = {"subj": subj, 'messages': messages,
               'participants': participants, 'classroom': classroom,
               'people': people, 'person': person}
    return render(request, 'subject.html', context)


def MyClass(request, pk):
    # create an instance of the of the specific classroom ou want to show using the pk
    classroom = Classroom.objects.get(id=pk)
    # pass the context to be rendered on the page
    subjects = Classroom.objects.all()
    participants = classroom.participants.all()
    posts = Post.objects.all()
    
    if request.method == 'POST':
        new_post = Post.objects.create(
            user=request.user,
            title=request.POST.get('post_title'),
            post_body=request.POST.get('content'),

        )
        return redirect('subject', pk=classroom.id)
    
    context = {"classroom": classroom, 'subjects': subjects,
               'participants': participants, 'posts': posts}
    return render(request, 'class.html', context)


def CreateClassroom(request):
    
    create = True
    # create an instance of the of the specific classroom
    form = ClassRoomForm
    # check if the method being returned by the url and the form on teh HTML is post
    all_subjects = Subject.objects.all()
    all_students = Person.objects.all()
    
    if request.method == 'POST':
        new_post = Post.objects.create(
            user=request.user,
            title=request.POST.get('title'),
            post_body=request.POST.get('post'),
            picture=request.POST.get('post_picture'),
            media=request.POST.get('post_media'),

        )
        return redirect('home')
    
    context = {'form': form, 'create': create,
               'all_subjects': all_subjects, 'all_students': all_students}
    return render(request, 'classroom_form.html', context)



def UpdateClassroom(request, pk):
    create = False
    room = Classroom.objects.get(id=pk)

    # Check if the user trying to update is authorized
    if not request.user.is_superuser:
        return HttpResponseForbidden("You are not authorized to edit this Classroom.")

    if request.method == "POST":
        form = ClassRoomForm(request.POST, instance=room)
        if form.is_valid():
            # Delete the existing instance
            room.delete()

            # Save the updated form as a new instance
            new_instance = form.save(commit=False)
            new_instance.id = pk  # Set the id to the original id
            new_instance.save()

            # Redirect to the Home page on success
            return redirect('home')
    else:
        form = ClassRoomForm(instance=room)

    context = {'form': form, 'create': create}
    return render(request, 'classroom_form.html', context)



def DeleteClassroom(request, pk):
    # create an instance of the of the specific classroom ou want to delete using the pk
    room = Classroom.objects.get(id=pk)
    
    if request.user.is_superuser != True:
        return HttpResponseForbidden("You are not authorized to delete this Classroom.")
    
    if request.method == "POST":
        room.delete()
        return redirect('home')

    return render(request, 'delete_classroom.html', {'obj': room})

def MySubjects(request):
    
    me = Person.objects.get(id=request.user.pk)
    subjects = Subject.objects.all()
    my_class = request.user.my_class
    context = {'subjects': subjects, 'my_class': my_class}
    return render(request, 'my_subjects.html', context)