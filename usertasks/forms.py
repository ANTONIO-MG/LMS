from django import forms
from django.forms import ModelForm
from .models import TODO
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div, Submit


class TodoForm(ModelForm):
    class Meta:
        model = TODO
        fields = '__all__'
        exclude = ['user', 'status']

        widgets = {
            'task_date': forms.DateInput(attrs={'type': 'date'}),
        }

        def __init__(self, *args, **kwargs):
            super(TodoForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_method = 'post'
            self.helper.layout = Layout(
                Field('title', css_class='form-control'),
                Field('description', css_class='form-control'),
                Field('subject', css_class='form-control'),
                Field('task_date', css_class='form-control'),
                Field('user', css_class='form-control'),
            )
        
