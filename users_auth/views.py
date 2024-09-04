from datetime import datetime, timedelta
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.shortcuts import redirect, render, get_object_or_404
from .forms import PersonEditForm
from usertasks.models import TaskCompletion, TODO, TimelineItem
from communication.models import Notification, Message, Post
from communication.forms import MessageForm
from usertasks.models import Reminder
from usertasks.forms import ReminderForm
from users_auth.models import Classroom, Person, Subject
from .date_time import get_date_at_midnight
from django.db.models import Q
from django.utils.timezone import now

# View for the landing page
def landing_page_view(request):
    return render(request, 'landing_page.html')

# The homepage view
@login_required
def Home(request):
    """
    Home view that displays the user's dashboard with classrooms, notifications, tasks, and reminders.
    """
    # Get the current user
    me = Person.objects.get(user=request.user)
    classrooms = Classroom.objects.all()
    notifications = Notification.objects.all()[:3]
    assigned_tasks = TaskCompletion.objects.filter(user=me.id)[:6]
    subjects = Subject.objects.all()
    my_class = me.my_class

    # Date functions
    current_date = now().date()
    current_date_plus = current_date + timedelta(days=1)
    current_date_minus = current_date - timedelta(days=1)

    form = ReminderForm()
    # Check if the user has updated their profile; if not, redirect to profile update
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = ReminderForm(request.POST)
            if form.is_valid():
                reminder = form.save(commit=False)  # Create form instance but don't save yet
                reminder.user = me  # Set the user field to the requesting user
                reminder.save()  # Save the form instance
                return redirect('home')  # Redirect to the home page after saving the reminder
    else:
        form = ReminderForm()

    reminders = Reminder.objects.all().order_by('-created_at')
    
    # Calculate time since creation for each reminder
    for reminder in reminders:
        reminder.time_since = (now() - reminder.created_at).total_seconds() / 60

    # Get the current user status, if profile is updated or not
    user_status = Person.objects.get(user=request.user)
    if not user_status.profile_status:
        return redirect('edit_profile', pk=user_status.id)

    context = {
        "classrooms": classrooms,
        "notifications": notifications,
        "subjects": subjects,
        'my_class': my_class,
        'assigned_tasks': assigned_tasks,
        "me": me,
        'form': form,
        'reminders': reminders,
        'current_date': current_date,
        'current_date_plus': current_date_plus,
        'current_date_minus': current_date_minus,
    }
    return render(request, 'home.html', context)

# View to delete a reminder
@login_required
def delete_reminder(request, reminder_id):
    reminder = get_object_or_404(Reminder, id=reminder_id)
    reminder.delete()
    return redirect('home')

# View for the chat functionality
@login_required
def Chat_View(request, pk):
    # Fetch the recipient (user you're chatting with) based on the primary key
    recipient = get_object_or_404(Person, id=pk)
    
    # Get the current person (the user who is logged in)
    current_person = get_object_or_404(Person, user=request.user)

    # Handle message submission
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = current_person
            new_message.recipient = recipient
            new_message.save()
            return redirect('chat_view', pk=pk)  # Redirect to the same chat view after sending the message
    else:
        form = MessageForm()

    # Fetch all messages between the current user and the recipient
    messages = Message.objects.filter(
        (Q(sender=current_person) & Q(recipient=recipient)) |
        (Q(sender=recipient) & Q(recipient=current_person))
    ).order_by('created_at')

    # Get all users who have exchanged messages with the current user
    chat_users = set()
    sent_messages = Message.objects.filter(sender=current_person).exclude(recipient=None)
    received_messages = Message.objects.filter(recipient=current_person)
    
    # Add the recipients from sent messages and senders from received messages to the chat_users set
    for message in sent_messages:   
        chat_users.add(message.recipient)
    for message in received_messages:
        chat_users.add(message.sender)

    # Check if there is a message ID in the request to mark as read
    message_id = request.GET.get('message_id')
    if message_id:
        # Fetch the message that needs to be marked as read
        message = get_object_or_404(Message, id=message_id, recipient=current_person)
        if not message.read_status:
            message.read_status = True
            message.save()
        return JsonResponse({'status': 'success', 'message': 'Message marked as read.'})

    # Render the chat template with the messages and recipient
    return render(request, 'chat.html', {
        'messages': messages,
        'recipient': recipient,
        'current_person': current_person,
        'chat_users': chat_users,
        'form': form
    })

# View for the user profile
@login_required
def Profile(request, pk):
    if request.user.is_authenticated:
        me = Person.objects.get(user=request.user)
        all_posts = Post.objects.all()
        all_users = Person.objects.all()
        subjects = me.participants.all()
        classrooms = Classroom.objects.all()
        messages = Message.objects.all()
        notifications = Notification.objects.all()[:5]
        my_class = me.my_class
        current_date = get_date_at_midnight
        timeline_items = TimelineItem.objects.filter(user=me).all()
        context = {
            "classrooms": classrooms, 
            "messages": messages,
            "notifications": notifications,
            'me': me, 
            'subjects': subjects,
            'all_users': all_users, 
            'all_posts': all_posts, 
            'my_class': my_class,
            'timeline_items': timeline_items,
            'current_date': current_date
        }  

        return render(request, 'profile.html', context)

# View to edit the user profile
@login_required
def EditProfile(request, pk):
    person = get_object_or_404(Person, id=pk)  # Fetch the Person instance with the given id (pk)
    
    if request.method == "POST":
        # When the form is submitted
        form = PersonEditForm(request.POST, request.FILES, instance=person)
        if form.is_valid():
            try:
                # Save the form but don't commit changes to the database yet
                new_user = form.save(commit=False)
                new_user.user = request.user
                new_user.email = request.user.email

                # Retrieve the selected country code from the form data
                selected_country_code = request.POST.get('country_code')

                # Save the changes to the database while updating the user profile status
                new_user.profile_status = True
                new_user.save()

                # Handle class and subjects
                selected_class = new_user.my_class
                if selected_class:
                    subjects_for_class = selected_class.subjects.all()
                    if subjects_for_class.exists():
                        for subject in subjects_for_class:
                            subject.participants.add(new_user)
                    selected_class.participants.add(new_user)

                return redirect('profile', pk=pk)  # Redirect to the Profile view on success
            
            except Exception as e:
                # Handle any exceptions that might occur during the form save process
                print(f"An error occurred: {e}")
                context = {'form': form, 'error_message': str(e)}
                return render(request, 'edit_profile.html', context)
    
    else:
        # When the form is first loaded (GET request), pre-populate it with the person's data
        form = PersonEditForm(instance=person)

    # Render the form with the pre-populated data
    context = {'form': form}
    return render(request, 'edit_profile.html', context)

# View for a specific subject
@login_required
def MySubject(request, pk):
    me = Person.objects.get(user=request.user)
    subj = Subject.objects.get(id=pk)
    messages = Message.objects.all()
    people = Person.objects.all()
    person = Person.objects.get(user=request.user.id)
    participants = subj.participants.all()
    classroom = Classroom.objects.get(id=subj.class_room.id)  # Corrected line

    if request.method == 'POST':
        new_message = Message.objects.create(
            user=me,
            content=request.POST.get('message'),  # Corrected line
            subject=subj,
            class_room=subj.class_room
        )
        return redirect('subject', pk=subj.id)

    context = {
        "subj": subj,
        'messages': messages,
        'participants': participants,
        'classroom': classroom,
        'people': people,
        'person': person
    }
    return render(request, 'subject.html', context)


@login_required
def MyClass(request, pk):
    """
    View to display a specific classroom and handle post creation within that classroom.
    
    Args:
        request: The HTTP request object.
        pk: The primary key of the classroom to be displayed.
    
    Returns:
        A rendered HTML page displaying the classroom details, subjects, participants, and posts.
    """
    # Get the current logged-in user
    me = Person.objects.get(user=request.user)
    
    # Get the specific classroom using the primary key (pk)
    classroom = Classroom.objects.get(id=pk)
    
    # Get all subjects (classrooms), participants of the specific classroom, and all posts
    subjects = Classroom.objects.all()
    participants = classroom.participants.all()
    posts = Post.objects.all()
    
    # Handle post creation if the request method is POST
    if request.method == 'POST':
        new_post = Post.objects.create(
            user=me,
            title=request.POST.get('post_title'),
            post_body=request.POST.get('content'),
        )
        # Redirect to the subject view of the classroom after creating the post
        return redirect('subject', pk=classroom.id)
    
    # Context to be passed to the template
    context = {
        "classroom": classroom,
        'subjects': subjects,
        'participants': participants,
        'posts': posts
    }
    
    # Render the class.html template with the context
    return render(request, 'class.html', context)

def password_reset_from_key(request, uidb36=None, key=None):
    """
    View to handle password reset from a key.
    
    Args:
        request: The HTTP request object.
        uidb36: The base36 encoded user ID.
        key: The password reset key.
    
    Returns:
        A rendered HTML page for password reset.
    """
    # Context to be passed to the template
    context = {
        'uidb36': uidb36,
        'key': key,
    }
    
    # Render the password_reset_from_key.html template with the context
    return render(request, 'account/password_reset_from_key.html', context)
