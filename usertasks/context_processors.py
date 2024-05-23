# from .models import Person, Classroom, Subject
# from communication.models import Message, Notification
# from usertasks.models import TODO, TaskCompletion
# """
#     this imports the models and then creates general context that will be sent to all the pages to be rendared
# """

# def global_context(request):
#     if request.user.is_authenticated:
#         me = Person.objects.get(user=request.user)
#         classrooms = Classroom.objects.all()
#         class_messages = messages = Message.objects.filter(class_room=me.my_class)
#         messages = Message.objects.all()
#         notifications = Notification.objects.all()
#         tasks = TODO.objects.all()
#         all_users = Person.objects.all()
#         assigned_task = TaskCompletion.objects.filter(user=me)
#         subjects = Subject.objects.all()
#         my_class = me.my_class

#         messages_count = class_messages.count
#         notification_count = notifications.count
#         # all_notifications_count = int(messages_count) + int(notification_count)
#         last_message = class_messages.last
#         last_notifications = notifications.last
#         create = True

#         return {
#             "classrooms": classrooms,
#             "messages": messages,
#             "notifications": notifications,
#             "tasks": tasks,
#             "subjects": subjects,
#             "my_class": my_class,
#             "all_users": all_users,
#             "assigned_task": assigned_task,
#             "me": me,
#             "class_messages": class_messages,
#             "messages_count": messages_count,
#             "notification_count": notification_count,
#             'create': create,
#             # "all_notifications_count": all_notifications_count
#         }
#     return {}