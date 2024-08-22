from django import forms
from django.forms import ModelForm
from .models import Message, Notification
from users_auth.models import Classroom
from communication.models import Post


# form to create a classroom
class ClassRoomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = '__all__'

# form to create a message


class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        # Exclude specific fields
        exclude_fields = ['subject', 'sender', 'class_room', 'responce_to', 'recipient']
        for field_name in exclude_fields:
            if field_name in self.fields:
                del self.fields[field_name]

# form to create a Notification


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
        exclude = ['user']


