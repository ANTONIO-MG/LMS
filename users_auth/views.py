from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from pyexpat.errors import messages
from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render, get_object_or_404
from .  forms import PersonForm, PersonEditForm
from usertasks.models import TaskCompletion, TODO, TimelineItem
from communication.models import Notification, Message, Post
from communication.forms import MessageForm
from users_auth.models import Classroom, Person, Subject
from users_auth.countries import country_phone_codes
from .date_time import get_date_at_midnight
from threading import Thread
from django.db.models import Q




# The homepage view
def Home(request):
    """
    classroom: stores all the classroom as objects and can be queried
    messages: stores all the messages on teh database and can be queried
    """
    # check if the user has updated his profile if not take to profile update
    if request.user.is_authenticated:
        user_status = Person.objects.get(user=request.user)
        if not user_status.profile_status:
            return redirect('edit_profile', pk=user_status.id)

    # this are the things that will need to be on every view so that the sidebar and the header remain constant
    me = Person.objects.get(user=request.user)
    classrooms = Classroom.objects.all()
    messages = Message.objects.all()
    notifications = Notification.objects.all()[0:3]
    tasks = TODO.objects.all()
    assigned_task = TaskCompletion.objects.filter(user=me)
    subjects = Subject.objects.all()

    
    my_class = me.my_class

    context = {"classrooms": classrooms, "messages" : messages,
               "notifications" : notifications, "tasks": tasks,
               "subjects": subjects, 'my_class': my_class,
               'assigned_task': assigned_task,
               "me":me}
    return  render(request, 'home.html', context)


def Chat_View(request, pk):
    # Fetch the recipient (user you're chatting with) based on the primary key
    recipient = get_object_or_404(Person, id=pk)
    
    # Get the current person (the user who is logged in)
    current_person = get_object_or_404(Person, user=request.user)
    # Fetch all messages between the current user and the recipient

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
    

def Profile(request, pk):
    if request.user.is_authenticated:
        me = Person.objects.get(user=request.user)
        all_posts = Post.objects.all()
        all_users = Person.objects.all()
        subjects = me.participants.all()
        classrooms = Classroom.objects.all()
        messages = Message.objects.all()
        notifications = Notification.objects.all()[0:5]
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

        return render(request, 'profile.html', context)  # Added 'context' here


from django.shortcuts import render, redirect, get_object_or_404

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

                # Combine the country code with the contact number if a country code was selected
                if selected_country_code:
                    new_user.contact_number = combine_country_code(selected_country_code, new_user.contact_number)
                    new_user.emergency_contact = combine_country_code(selected_country_code, new_user.emergency_contact)

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
                context = {'form': form, "country_phone_codes": country_phone_codes, 'error_message': str(e)}
                return render(request, 'edit_profile.html', context)
    
    else:
        # When the form is first loaded (GET request), pre-populate it with the person's data
        form = PersonEditForm(instance=person)

    # Render the form with the pre-populated data
    context = {'form': form, "country_phone_codes": country_phone_codes}
    return render(request, 'edit_profile.html', context)


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
            class_room =subj.class_room
        )
        return redirect('subject', pk=subj.id)

    context = {"subj": subj, 'messages': messages,
               'participants': participants, 'classroom': classroom,
               'people': people, 'person': person}
    return render(request, 'subject.html', context)


def MyClass(request, pk):
    me = Person.objects.get(user=request.user)
    # create an instance of the of the specific classroom ou want to show using the pk
    classroom = Classroom.objects.get(id=pk)
    # pass the context to be rendered on the page
    subjects = Classroom.objects.all()
    participants = classroom.participants.all()
    posts = Post.objects.all()
    
    if request.method == 'POST':
        new_post = Post.objects.create(
            user=me,
            title=request.POST.get('post_title'),
            post_body=request.POST.get('content'),

        )
        return redirect('subject', pk=classroom.id)
    
    context = {"classroom": classroom, 'subjects': subjects,
               'participants': participants, 'posts': posts}
    return render(request, 'class.html', context)

# Ensure that the view passing the context to the template includes uidb36 and key.
def password_reset_from_key(request, uidb36=None, key=None):
    context = {
        'uidb36': uidb36,
        'key': key,
    }
    return render(request, 'account/password_reset_from_key.html', context)

def combine_country_code(country, phone_number):
    try:
        # Ensure the country exists in the dictionary
        if country not in country_phone_codes:
            raise ValueError(f"Country '{country}' not found.")
        
        country_info = country_phone_codes[country]
        country_code = country_info["code"]
        example_number = country_info["example"]

        # Remove leading zero if present
        if phone_number.startswith('0'):
            phone_number = phone_number[1:]

        # Check if the phone number matches the length of the example number
        if len(phone_number) != len(example_number):
            raise ValueError(f"Phone number length for {country} should be {len(example_number)} digits.")

        # Check if the phone number matches the starting pattern of the example
        if not phone_number.startswith(example_number[:2]):
            raise ValueError(f"Phone number for {country} should start with '{example_number[:2]}'.")

        # Combine country code and phone number
        full_number = country_code + phone_number
        return full_number

    except ValueError as e:
        return str(e)

