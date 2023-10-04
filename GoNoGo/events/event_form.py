from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
  
# creating a form
class EventForm(forms.Form):
  
    title = forms.CharField(required=True, max_length=20)
    content = forms.CharField(max_length=500)
    location = forms.CharField(max_length=50)
    date = forms.DateField(required=True)
    time = forms.TimeField(required=True)
    attendees = forms.CharField(required=True)

    def clean_attendees(self):
        emails = self.cleaned_data['attendees'].split(',')
        for email in emails:
            try:
                validate_email(email.strip())
            except ValidationError:
                raise forms.ValidationError(f"{email} is not a valid email address")
        return emails

    

    


