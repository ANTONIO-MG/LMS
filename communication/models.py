from django.db import models
from users_auth.models import Person, Classroom, Subject

Notification_Groups = [
    ('educators', 'Educators'),
    ('students', 'Students'),
    ('all', 'All'),
    ('class', 'Class'),
    ('subject', 'Subject'),
]

Post_Groups = [
    ('public', 'Puplic'),
    ('Private', 'Private'),
    ('class', 'Class'),
    ('subject', 'Subject'),
]

COMMS_STATUS = [
    ('read', 'Read'),
    ('unread', 'Unread'),
    ('replied', 'Replied'),
]

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True)
    class_room = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True)
    content = models.TextField()
    status = models.CharField(max_length=15, choices=COMMS_STATUS, default='unread')
    responce_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.content[:50])
    
    
class Notification(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    notification_group = models.CharField(max_length=25, choices=Notification_Groups, default='all')
    read_count = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return str(self.title)


class Post(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="user_posts")
    title = models.CharField(max_length=100, blank=True, null=True)
    post_body = models.TextField()
    picture = models.ImageField(upload_to='post_pics/', null=True, blank=True)
    media = models.FileField(upload_to='audio_files/', blank=True, null=True)
    status = models.CharField(max_length=15, choices=COMMS_STATUS, default='unread')
    notification_group = models.CharField(max_length=25, choices=Post_Groups, default='public')
    likes = models.IntegerField(default=0)
    comments = models.ManyToManyField(Message, related_name="post_comments", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return f'{self.title} - {self.user}'