# forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'matriculation_number', 'level', 'faculty', 'department', 'profile_picture']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        # Make 'username' field read-only
        self.fields['username'].widget.attrs['readonly'] = True

        # Make other fields read-only
        for field_name in self.fields:
            if field_name != 'username':
                self.fields[field_name].widget.attrs['readonly'] = True
