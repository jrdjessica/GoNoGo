from django import forms
  
# creating a form
class EventForm(forms.Form):
  
    title = forms.CharField(required=True, max_length=20)
    content = forms.CharField(max_length=500)
    location = forms.CharField(max_length=50)
    date = forms.DateField(required=True)
    time = forms.TimeField(required=True)
    attendees = forms.EmailField(required=True)
    

    


