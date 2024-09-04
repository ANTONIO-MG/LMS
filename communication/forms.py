from django import forms
from django.forms import ModelForm
from .models import Message, Notification
from users_auth.models import Classroom
from communication.models import Post

# Form to create a Classroom
class ClassRoomForm(ModelForm):
    class Meta:
        model = Classroom  # Specify the model to use
        fields = '__all__'  # Include all fields from the model

# Form to create a Post
class PostForm(ModelForm):
    class Meta:
        model = Post  # Specify the model to use
        fields = '__all__'  # Include all fields from the model

# Form to create a Message
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message  # Specify the model to use
        fields = ['content']  # Only include the 'content' field

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        # Modify the 'content' field to use a Bootstrap input field
        self.fields['content'].widget = forms.TextInput(attrs={
            'class': 'form-control form-control-md',  # Add Bootstrap class for styling
            'placeholder': 'Type a message...',  # Placeholder text for the input field
            'autocomplete': 'on',  # Enable autocomplete
            'autofocus': 'autofocus',  # Autofocus the input field when the form is loaded
        })

# Form to create a Notification
class NotificationForm(ModelForm):
    class Meta:
        model = Notification  # Specify the model to use
        fields = '__all__'  # Include all fields from the model
        exclude = ['user']  # Exclude the 'user' field from the form