from django.db import models
from users_auth.models import Person, Classroom, Subject

# Choices for notification groups
Notification_Groups = [
    ('educators', 'Educators'),
    ('students', 'Students'),
    ('all', 'All'),
    ('class', 'Class'),
    ('subject', 'Subject'),
]

# Choices for post groups
Post_Groups = [
    ('public', 'Puplic'),
    ('Private', 'Private'),
    ('class', 'Class'),
    ('subject', 'Subject'),
]

# Choices for communication status
COMMS_STATUS = [
    ('read', 'Read'),
    ('unread', 'Unread'),
    ('replied', 'Replied'),
]

# Model to represent a message
class Message(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="sent_messages", blank=True, null=True)
    recipient = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="received_messages", blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, blank=True, null=True)
    class_room = models.ForeignKey(Classroom, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()  # Content of the message
    read_status = models.BooleanField(default=False)  # Read status of the message
    response_to = models.ForeignKey('self', on_delete=models.CASCADE, related_name="replies", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the message was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the message was last updated

    class Meta:
        ordering = ['created_at']  # Order messages by creation date

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"  # String representation of the message

# Model to represent a notification
class Notification(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE)  # User associated with the notification
    title = models.CharField(max_length=255)  # Title of the notification
    content = models.TextField()  # Content of the notification
    notification_group = models.CharField(max_length=25, choices=Notification_Groups, default='all')  # Group to which the notification belongs
    read_count = models.IntegerField(default=0)  # Count of how many times the notification has been read
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the notification was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the notification was last updated

    class Meta:
        ordering = ['-updated_at', '-created_at']  # Order notifications by last updated and creation date

    def __str__(self):
        return str(self.title)  # String representation of the notification

# Model to represent a post
class Post(models.Model):
    user = models.ForeignKey(Person, on_delete=models.CASCADE, related_name="user_posts")  # User who created the post
    title = models.CharField(max_length=100, blank=True, null=True)  # Title of the post
    post_body = models.TextField()  # Body content of the post
    picture = models.ImageField(upload_to='post_pics/', null=True, blank=True)  # Optional picture associated with the post
    media = models.FileField(upload_to='audio_files/', blank=True, null=True)  # Optional media file associated with the post
    status = models.CharField(max_length=15, choices=COMMS_STATUS, default='unread')  # Status of the post
    notification_group = models.CharField(max_length=25, choices=Post_Groups, default='public')  # Group to which the post belongs
    likes = models.IntegerField(default=0)  # Number of likes the post has received
    comments = models.ManyToManyField(Message, related_name="post_comments", blank=True)  # Comments associated with the post
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the post was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the post was last updated

    class Meta:
        ordering = ['-updated_at', '-created_at']  # Order posts by last updated and creation date

    def __str__(self):
        return f'{self.title} - {self.user}'  # String representation of the post