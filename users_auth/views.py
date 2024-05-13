from datetime import timezone
from pyexpat.errors import messages
from django.shortcuts import redirect, render
from .  forms import PersonForm, PersonEditForm
from usertasks.models import TaskCompletion, TODO
from communication.models import Notification, Message
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
    assigned_task = TaskCompletion.objects.filter(user=request.user)
    subjects = Subject.objects.all()
    me = Person.objects.get(id=request.user.pk)
    my_class = request.user.my_class
    print(my_class)
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
