# resources/forms.py
from django import forms
from .models import Resource, Rental, ResourceReview

class ResourceForm(forms.ModelForm):
    class Meta:
        model = Resource
        exclude = ('user',)
