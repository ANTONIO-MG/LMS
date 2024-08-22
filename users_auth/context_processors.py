from .models import Person, Classroom, Subject
from django.db.models import Q
from communication.forms import MessageForm
from communication.models import Message, Notification
from usertasks.models import TODO, TaskCompletion
from users_auth.country_code import country_phone_codes
from users_auth.users_informations import RACE, USER_TYPE_CHOICES, GENDER_CHOICES
from users_auth.countries import country_names
"""
    this imports the models and then creates general context that will be sent to all the pages to be rendared
"""

def global_context(request):

    if request.path.startswith('/admin/'):
        return {}
    else:
        if request.user.is_authenticated:
            me = Person.objects.get(user=request.user)
            classrooms = Classroom.objects.all()
            class_messages = Message.objects.filter(class_room=me.my_class)
            subject_messages = Message.objects.filter(subject__class_room=me.my_class)
            messages = Message.objects.all()
            notifications = Notification.objects.all()
            tasks = TODO.objects.all()
            all_users = Person.objects.all()
            assigned_tasks = TaskCompletion.objects.filter(user=me)[:6]
            subjects = Subject.objects.all()
            my_class = me.my_class

            # count males versus females participants
            male_count = my_class.participants.filter(gender='male').count()
            female_count = my_class.participants.filter(gender='female').count()

            messages_count = class_messages.count
            notification_count = notifications.count
            # all_notifications_count = int(messages_count) + int(notification_count)
            last_message = class_messages.last
            last_notifications = notifications.last
            races = RACE
            user_types = USER_TYPE_CHOICES
            genders = GENDER_CHOICES
            countries = country_names

            return {
                "classrooms": classrooms,
                "messages": messages,
                "notifications": notifications,
                "tasks": tasks,
                "subjects": subjects,
                "my_class": my_class,
                "all_users": all_users,
                "assigned_tasks": assigned_tasks,
                "me": me,
                # 'all_notifications_count': all_notifications_count,
                'last_message': last_message,
                'last_notifications': last_notifications,
                "class_messages": class_messages,
                "subject_messages": subject_messages,
                "messages_count": messages_count,
                "notification_count": notification_count,
                "races": races,
                "user_types": user_types,
                "genders": genders,
                "countries": countries,
                "male_count": male_count,
                "female_count": female_count
                }
        return {}
    
def chat_context(request):
    if request.user.is_authenticated:
        recipient_id = request.GET.get('recipient_id')
        recipient = None
        messages = []
        form = None

        if recipient_id:
            try:
                recipient = Person.objects.get(id=recipient_id)
                messages = Message.objects.filter(
                    (Q(sender=request.user) & Q(recipient=recipient)) |
                    (Q(sender=recipient) & Q(recipient=request.user))
                ).order_by('created_at')
            except Person.DoesNotExist:
                pass

            form = MessageForm()

        return {
            'chat_messages': messages,
            'chat_form': form,
            'chat_recipient': recipient
        }
    
    return {}