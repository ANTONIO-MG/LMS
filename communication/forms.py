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


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']  # Only include the 'content' field

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        # Modify the 'content' field to use a Bootstrap input field
        self.fields['content'].widget = forms.TextInput(attrs={
            'class': 'form-control form-control-md',
            'placeholder': 'Type a message...',
            'autocomplete': 'on',
            'autofocus': 'autofocus',
        })

# form to create a Notification


class NotificationForm(ModelForm):
    class Meta:
        model = Notification
        fields = '__all__'
        exclude = ['user']


