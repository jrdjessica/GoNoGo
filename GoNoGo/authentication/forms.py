from django import forms
from django.utils.safestring import mark_safe

# Log In Form


class LogInForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput(), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs.update({'placeholder': 'Your Email'})
        self.fields['password'].widget.attrs.update(
            {'placeholder': 'Your Password'})

# Sign Up Form


class SignUpForm(forms.Form):
    first_name = forms.CharField(
        max_length=50, label=mark_safe('First Name: <br />'))
    last_name = forms.CharField(
        max_length=50, label=mark_safe('Last Name: <br />'))
    email = forms.EmailField(required=True, label=mark_safe('Email: <br />'))
    password = forms.CharField(widget=forms.PasswordInput(
    ), required=True, label=mark_safe('Password: <br />'))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_suffix = ""
