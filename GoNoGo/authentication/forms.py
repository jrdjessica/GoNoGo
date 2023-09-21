from django import forms
  
# creating a form
class LogInForm(forms.Form):
  
    email = forms.EmailField(required=True)
    password = forms.CharField(widget = forms.PasswordInput(),required=True)


class SignUpForm(forms.Form):
    first_name = forms.CharField(max_length = 50)
    last_name = forms.CharField(max_length = 50)
    email = forms.EmailField(required=True)
    password = forms.CharField(widget = forms.PasswordInput(),required=True)