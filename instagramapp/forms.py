from django import forms
from .models import Profile, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']


class ProfileEdit(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['status']


class SearchForm(forms.Form):
    search = forms.CharField()


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
