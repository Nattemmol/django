# core/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'username', 'phone')

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'photo', 'languages', 'badges', 'skills_offered', 'skills_requested']
