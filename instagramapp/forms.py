from django import forms
from .models import User, Profile
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2']


class ProfileEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['status']


class SearchForm(forms.Form):
    search = forms.CharField()
