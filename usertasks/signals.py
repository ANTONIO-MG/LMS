from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.conf import settings
from users_auth.models import Person
from usertasks.models import TODO, TaskCompletion, TimelineItem
from communication.models import Message, Notification
import os


# # Signal handler for task creation and update
# @receiver(post_save, sender=TODO)
# def handle_task_save(sender, instance, created, **kwargs):
#     selected_subject = instance.subject
#     participants = selected_subject.participants.all()

#     if created:
#         # Create TaskCompletion objects for each participant
#         task_completions = []
#         for participant in participants:
#             task_completions.append(TaskCompletion(
#                 user=participant,
#                 task=instance,
#                 start_date=instance.start_date,
#                 end_date=instance.end_date,
#             ))
#         TaskCompletion.objects.bulk_create(task_completions)

#     else:
#         # Update TaskCompletion objects for existing task
#         TaskCompletion.objects.filter(task=instance).update(
#             start_date=instance.start_date,
#             end_date=instance.end_date,
#         )

#     # Handle cases where participants are added after task creation
#     existing_task_completions = TaskCompletion.objects.filter(task=instance)
#     existing_participants = existing_task_completions.values_list('user_id', flat=True)

#     new_participants = participants.exclude(id__in=existing_participants)
#     if new_participants.exists():
#         task_completions = [
#             TaskCompletion(
#                 user=participant,
#                 task=instance,
#                 start_date=instance.start_date,
#                 end_date=instance.end_date,
#             ) for participant in new_participants
#         ]
#         TaskCompletion.objects.bulk_create(task_completions)

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
