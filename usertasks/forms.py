from django import forms
from django.forms import ModelForm
from .models import TODO, Reminder


class TodoForm(ModelForm):
    class Meta:
        model = TODO
        fields = '__all__'
        exclude = ['user', 'status']

        widgets = {
            'task_date': forms.DateInput(attrs={'type': 'date'}),
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TodoForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs.update({'class': 'form-control'})
        self.fields['description'].widget.attrs.update({'class': 'form-control'})
        self.fields['subject'].widget.attrs.update({'class': 'form-control'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control'})
        

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['message']