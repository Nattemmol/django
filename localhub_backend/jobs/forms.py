# jobs/forms.py
from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        exclude = ('user',)

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        exclude = ('user', 'status')
