# bellow are the list of classes that map data to teh database
from django.db import models
# Create your models here.
from users_auth.models import Person, Subject
from django.conf import settings
from django.templatetags.static import static


TASK_STATUS = [
    ('completed', 'Completed'),
    ('uncompleted', 'Uncompleted'),
    ('upcoming', 'Upcoming'),
]

COMMS_STATUS = [
    ('read', 'Read'),
    ('unread', 'Unread'),
    ('replied', 'Replied'),
    ('sent', 'Sent'),
]

TIMELINE_ITEMS = [
    ('message', 'Message'),
    ('Notification', 'Notification'),
    ('task', 'Task'),
]


# Create your models here.
class TODO(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return str(self.title)

  
class TaskCompletion(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    task = models.ForeignKey(TODO, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=TASK_STATUS, default='sent')
    score = models.IntegerField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f'{self.task} - {self.user}'
    

class TimelineItem(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.CharField(max_length=200, null=True, blank=True)
    item_id = models.PositiveIntegerField()
    category = models.CharField(max_length=15, choices=
        TIMELINE_ITEMS, default='None')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f'{self.title} - {self.category  } - {self.user.username}'
    

class Reminder(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.message