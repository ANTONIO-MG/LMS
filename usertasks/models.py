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


# Create your models here.
class TODO(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    status = models.CharField(max_length=15, choices=TASK_STATUS, default='sent')
    task_date = models.DateTimeField()
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
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f'{self.user} - {self.task}'
    
class Post(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True)
    post_body = models.TextField()
    picture = models.ImageField(
        upload_to='post_pics/', null=True, blank=True)
    media = models.FileField(upload_to='audio_files/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=
        COMMS_STATUS, default='sent')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f'{self.title} - {self.user  }'