from .models import Person, Classroom, Subject
from communication.models import Message, Notification
from usertasks.models import TODO
from users_auth.users_informations import RACE, USER_TYPE_CHOICES, GENDER_CHOICES
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
            subjects = Subject.objects.all()

            # count males versus females participants
            # Initialize counters
            male_count = 0
            female_count = 0

            # Get all classrooms
            classrooms = Classroom.objects.all()

            # Iterate through each classroom
            for classroom in classrooms:
                # Get participants of the classroom
                participants = classroom.participants.all()

                # Count males and females among the participants
                t_male_count = participants.filter(gender='male').count()
                t_female_count = participants.filter(gender='female').count()

                # Add to the total counts
                male_count += t_male_count
                female_count += t_female_count

            messages_count = class_messages.count
            notification_count = notifications.count
            last_message = class_messages.last
            last_notifications = notifications.last
            races = RACE
            user_types = USER_TYPE_CHOICES
            genders = GENDER_CHOICES
            
            return {
                "classrooms": classrooms,
                "messages": messages,
                "notifications": notifications,
                "tasks": tasks,
                "subjects": subjects,
                "all_users": all_users,
                "me": me,
                'last_message': last_message,
                'last_notifications': last_notifications,
                "class_messages": class_messages,
                "subject_messages": subject_messages,
                "messages_count": messages_count,
                "notification_count": notification_count,
                "races": races,
                "user_types": user_types,
                "genders": genders,
                "male_count": male_count,
                "female_count": female_count
                }
        return {}
    
