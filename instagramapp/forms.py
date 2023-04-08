from django import forms
from .models import Comment, Post, Message
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password1', 'password2', 'email']
        widgets = {'username': forms.TextInput(attrs={'class': 'log_f'}),
                   'email': forms.TextInput(attrs={'class': 'log_f'}),
                   'first_name': forms.TextInput(attrs={'class': 'log_f'}),
                   'last_name': forms.TextInput(attrs={'class': 'log_f'}),
                   'password1': forms.PasswordInput(attrs={'class': 'log_f'}),
                   'password2': forms.PasswordInput(attrs={'class': 'log_f'})}


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': "form_e", 'placeholder': 'Search'}))


class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {'username': forms.TextInput(attrs={'class': 'log_f'}),
                   'password': forms.PasswordInput(attrs={'class': 'log_f'})}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {'body': forms.TextInput(attrs={
                   'class': "form_e",
                   'placeholder': 'Add a comment...'})}


class AddPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image']
        widgets = {'image': forms.FileInput(attrs={
                   'class': 'file_inpt'})}


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'description']
        widgets = {'description': forms.Textarea(attrs={'cols': 30, 'rows': 3}),
                   'image': forms.FileInput(attrs={'class': 'file_inpt'})}


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {'username': forms.TextInput(attrs={'class': 'log_f'}),
                   'email': forms.TextInput(attrs={'class': 'log_f'}),
                   'first_name': forms.TextInput(attrs={'class': 'log_f'}),
                   'last_name': forms.TextInput(attrs={'class': 'log_f'})}


class ChatForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {'body': forms.TextInput(attrs={'class': "form_e", 'placeholder': 'Type'})}
