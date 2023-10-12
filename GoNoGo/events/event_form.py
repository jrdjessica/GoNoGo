from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from .models import Event
from django.forms import DateInput

# Event Form


class EventForm(forms.ModelForm):

    class Meta:
        model = Event
        fields = ['title', 'content', 'location', 'date', 'time', 'attendees']
        widgets = {
            'date': DateInput(attrs={'type': 'date'}),
            'time': DateInput(attrs={'type': 'time'}),
        }
