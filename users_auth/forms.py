from django import forms
from django.forms import ModelForm
from .models import Classroom, Person
from communication.forms import MessageForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit
from phonenumber_field.formfields import PhoneNumberField
from phonenumber_field.widgets import PhoneNumberPrefixWidget



# form to create a classroom
class ClassRoomForm(ModelForm):
    class Meta:
        model = Classroom
        fields = '__all__'


    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)
        # Exclude specific fields
        exclude_fields = ['subject', 'subjects', 'user', 'class_room']
        for field_name in exclude_fields:
            if field_name in self.fields:
                del self.fields[field_name]


class PersonForm(forms.ModelForm):
    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['user', 'is_staff', 'is_active', 'created_at', 'updated_at',
                   'bio', 'profile_picture', 'last_login', 'subjects', 'password', 'email']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('first_name', css_class='form-control'),
            Field('last_name', css_class='form-control'),
            Field('nickname', css_class='form-control'),
            Field('date_of_birth', css_class='form-control'),
            Field('gender', css_class='form-control'),
            Field('race', css_class='form-control'),
            Field('user_type', css_class='form-control'),
            Field('my_class', css_class='form-control'),
            Field('contact_number', css_class='form-control'),
            Field('emergency_contact', css_class='form-control'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )

    my_class = forms.ModelChoiceField(
        queryset=Classroom.objects.all(), required=True)


class PersonEditForm(ModelForm):
    """ this one is used for user profile editor"""

    contact_number = PhoneNumberField(region='US', widget=PhoneNumberPrefixWidget())
    emergency_contact = PhoneNumberField(region='US', widget=PhoneNumberPrefixWidget())


    class Meta:
        model = Person
        fields = '__all__'
        exclude = ['password', 'user_type', 'subjects', 'is_staff', 'is_active', 'groups', 'last_login',
                   'user_permissions', 'is_superuser', 'email', 'my_class', 'user', 'user_type', 'my_class']
        
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super(PersonEditForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.layout = Layout(
            Field('first_name', css_class='form-control'),
            Field('last_name', css_class='form-control'),
            Field('nickname', css_class='form-control'),
            Field('date_of_birth', css_class='form-control'),
            Field('gender', css_class='form-control'),
            Field('race', css_class='form-control'),
            Field('contact_number', css_class='form-control'),
            Field('emergency_contact', css_class='form-control'),
            Submit('submit', 'Submit', css_class='btn btn-primary')
        )