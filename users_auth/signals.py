from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.conf import settings
from .models import Person, Classroom
from usertasks.models import TODO, TaskCompletion

# Helper function to create or ensure a Person profile
def create_or_get_person(user):
    no_class, created = Classroom.objects.get_or_create(name='NO CLASS')
    person, created = Person.objects.get_or_create(
        user=user,
        defaults={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'nickname': user.username,
            'email': user.email,
            'my_class': no_class,
        }
    )
    if created:
        no_class.participants.add(person)
    return person

# Signal handler for user signup
@receiver(user_signed_up)
def handle_user_signed_up(request, user, **kwargs):
    create_or_get_person(user)
    print("##############################################################")
    print("# User signed up and 'NO CLASS' was checked.                 #")
    print("##############################################################")

# Signal handler for user login
@receiver(user_logged_in)
def handle_user_logged_in(request, user, **kwargs):
    create_or_get_person(user)
    print("##############################################################")
    print("# User logged in and 'NO CLASS' was checked.                 #")
    print("##############################################################")

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
        print("##############################################################")
        print("# New task created and assigned to all participants.        #")
        print("##############################################################")
    else:
        TaskCompletion.objects.filter(task=instance).update(
            start_date=instance.start_date,
            end_date=instance.end_date,
        )
        print("##############################################################")
        print("# Task updated and re-assigned to all participants.         #")
        print("##############################################################")
