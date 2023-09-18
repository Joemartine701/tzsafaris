from django import forms
from django.contrib.auth import get_user_model

class UserRegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(max_length=254, required=True)
    phone = forms.CharField(max_length=15, required=True)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, required=True)
    # Add any other fields you want to include in the registration form

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Email already registered.')
        return email