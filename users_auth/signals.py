from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.conf import settings
from .models import Person, Classroom, Subject
from usertasks.models import TODO, TaskCompletion, TimelineItem
from communication.models import Message, Notification
import os

# Helper function to create or ensure a Person profile
def create_or_get_person(user):
    """
    Creates or retrieves a Person profile for the given user.
    Also ensures that the user is added to the default classrooms and subjects.
    """
    # Get or create the default classrooms
    no_class1, created = Classroom.objects.get_or_create(name='BASE CLASS', description="This is the default class for all users")
    no_class2, created = Classroom.objects.get_or_create(name='GOBAL CLASS', description="This is a testing class")
    
    # Default profile picture path
    default_image_path = os.path.join('default.png')
    
    # Get or create the Person profile
    person, created = Person.objects.get_or_create(
        user=user,
        defaults={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'nickname': user.username,
            'email': user.email,
            'my_class': no_class1,
            'profile_picture': default_image_path
        }
    )
    
    # Add the person to the BASE CLASS participants if the Person object was just created
    if created:
        no_class1.participants.add(person)
        
        # Create the two subjects under the BASE CLASS
        Subject.objects.get_or_create(name='General Information', class_room=no_class1)
        Subject.objects.get_or_create(name='Special Information', class_room=no_class1)
    
    return person

# Signal handler for user signup
@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    """
    Signal handler that is triggered when a user signs up.
    Ensures that a Person profile is created for the user.
    """
    create_or_get_person(user)

# Signal handler for user login
@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    """
    Signal handler that is triggered when a user logs in.
    Ensures that a Person profile is created for the user.
    """
    create_or_get_person(user)

# Signal handler for saving a Message
@receiver(post_save, sender=Message)
def create_or_update_timeline_for_message(sender, instance, created, **kwargs):
    """
    Signal handler that is triggered when a Message is saved.
    Creates or updates a TimelineItem for the message.
    """
    if created:
        TimelineItem.objects.create(
            user=instance.sender,
            title=f'Message: {instance.content[:50]}',
            content=instance.content,
            category='Message',
            item_id=instance.id
        )
    else:
        TimelineItem.objects.filter(item_type='Message', item_id=instance.id).update(
            updated_at=instance.updated_at,
            content=instance.content
        )

# Signal handler for saving a Notification
@receiver(post_save, sender=Notification)
def create_or_update_timeline_for_notification(sender, instance, created, **kwargs):
    """
    Signal handler that is triggered when a Notification is saved.
    Creates or updates a TimelineItem for the notification.
    """
    if created:
        TimelineItem.objects.create(
            user=instance.user,
            title=f'Notification: {instance.title}',
            content=instance.content,
            category='Notification',
            item_id=instance.id
        )
    else:
        TimelineItem.objects.filter(item_type='Notification', item_id=instance.id).update(
            updated_at=instance.updated_at,
            content=instance.content
        )

# Signal handler for saving a TaskCompletion
@receiver(post_save, sender=TaskCompletion)
def create_or_update_timeline_for_task_completion(sender, instance, created, **kwargs):
    """
    Signal handler that is triggered when a TaskCompletion is saved.
    Creates or updates a TimelineItem for the task completion.
    """
    if created:
        TimelineItem.objects.create(
            user=instance.user,
            title=f'TaskCompletion: Task ID {instance.task.id}',
            content=f'Task: {instance.task.title}, Status: {instance.status}',
            category='TaskCompletion',
            item_id=instance.id
        )
    else:
        TimelineItem.objects.filter(item_type='TaskCompletion', item_id=instance.id).update(
            updated_at=instance.updated_at,
            content=f'Task: {instance.task.title}, Status: {instance.status}'
        )

# Signal handler for saving a User
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler that is triggered when a User is saved.
    Creates or updates a Person profile for the user.
    """
    if created:
        Person.objects.create(user=instance)
    instance.profile.save()