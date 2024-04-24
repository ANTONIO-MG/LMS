from django import forms
from django.forms import ModelForm
from .models import Classroom, Person




# form to create a classroom
class ClassRoomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'


    # def __init__(self, *args, **kwargs):
    #     super(MessageForm, self).__init__(*args, **kwargs)
    #     # Exclude specific fields
    #     exclude_fields = ['subject', 'subjects', 'user', 'class_room']
    #     for field_name in exclude_fields:
    #         if field_name in self.fields:
    #             del self.fields[field_name]


class EditProfileForm(ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['last_name', 'gender',
                   'race', 'emergency_contact',
                   'is_staff', 'is_active',
                   'groups', 'last_login', 'subjects',
                   'user_permissions', 'is_superuser']



class PersonForm(ModelForm):
    """ this one is used for user registration"""
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['profile_picture', 'contact_number'
                   'user_category', 'last_name', 'gender',
                   'race', 'emergency_contact', 'profile_picture',
                   'is_staff', 'is_active', 'date_of_birth', 'first_name',
                   'groups', 'superuser', 'last_login', 'subjects',
                   'user_permissions', 'is_superuser', 'bio', 'date_joined', 'contact_number',]
    my_class = forms.ModelChoiceField(
        queryset=Classroom.objects.all(), required=False)


class PersonEditForm(ModelForm):
    """ this one is used for user profile editor"""
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['password', 'user_type', 'subjects', 'is_staff', 'is_active', 'groups', 'last_login',
                   'user_permissions', 'is_superuser', 'email']
    my_class = forms.ModelChoiceField(
        queryset=Classroom.objects.all(), required=False)