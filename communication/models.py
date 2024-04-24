from django.db import models
from users_auth.models import Person, Classroom, Subject

Notification_Groups = [
    ('educators', 'Educators'),
    ('students', 'Students'),
    ('all', 'All'),
]

# Create your models here.
class Message(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE)
    class_room = models.ForeignKey(
        Classroom, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return str(self.content[0:50])
    
    
class Notification(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    notification_group = models.CharField(
        max_length=25, choices=Notification_Groups, default='All')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at', '-created_at']

    def __str__(self):
        return str(self.title)
