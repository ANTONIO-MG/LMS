from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.conf import settings
from .models import Person, Classroom,Subject
from usertasks.models import TODO, TaskCompletion, TimelineItem
from communication.models import Message, Notification
import os

# Helper function to create or ensure a Person profile
def create_or_get_person(user):
    no_class1, created = Classroom.objects.get_or_create(name='BASE CLASS', description="This is the default class for all users")
    no_class2, created = Classroom.objects.get_or_create(name='GOBAL CLASS', description="This is a testing class")
    default_image_path = os.path.join('default.png')
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
    if created:
        no_class1.participants.add(person)

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
    create_or_get_person(user)


# Signal handler for user login
@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    create_or_get_person(user)



@receiver(post_save, sender=Message)
def create_or_update_timeline_for_message(sender, instance, created, **kwargs):
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

@receiver(post_save, sender=Notification)
def create_or_update_timeline_for_notification(sender, instance, created, **kwargs):
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

@receiver(post_save, sender=TaskCompletion)
def create_or_update_timeline_for_task_completion(sender, instance, created, **kwargs):
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


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Person.objects.create(user=instance)
    instance.profile.save()