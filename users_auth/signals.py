from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.conf import settings
from .models import Person, Classroom
from usertasks.models import TODO, TaskCompletion, TimelineItem
from communication.models import Message, Notification

# Helper function to create or ensure a Person profile
def create_or_get_person(user):
    no_class1, created = Classroom.objects.get_or_create(name='NO CLASS')
    no_class2, created = Classroom.objects.get_or_create(name='GOBAL CLASS')
    person, created = Person.objects.get_or_create(
        user=user,
        defaults={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'nickname': user.username,
            'email': user.email,
            'my_class': no_class1,
        }
    )
    if created:
        no_class1.participants.add(person)
    return person

# Signal handler for user signup
@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    create_or_get_person(user)


# Signal handler for user login
@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    create_or_get_person(user)


# Signal handler for task creation and update
@receiver(post_save, sender=TODO)
def handle_task_save(sender, instance, created, **kwargs):
    selected_subject = instance.subject
    participants = selected_subject.participants.all()

    if created:
        for participant in participants:
            TaskCompletion.objects.create(
                user=participant,
                task=instance,
                start_date=instance.start_date,
                end_date=instance.end_date,
            )
    else:
        TaskCompletion.objects.filter(task=instance).update(
            start_date=instance.start_date,
            end_date=instance.end_date,
        )


@receiver(post_save, sender=Message)
def create_or_update_timeline_for_message(sender, instance, created, **kwargs):
    if created:
        TimelineItem.objects.create(
            user=instance.user,
            title=f'Message: {instance.content[:50]}',
            content=instance.content,
            item_type='Message',
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
            item_type='Notification',
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
            item_type='TaskCompletion',
            item_id=instance.id
        )
    else:
        TimelineItem.objects.filter(item_type='TaskCompletion', item_id=instance.id).update(
            updated_at=instance.updated_at,
            content=f'Task: {instance.task.title}, Status: {instance.status}'
        )
