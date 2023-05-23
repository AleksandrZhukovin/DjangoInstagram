from django import forms
from accounts.models import User


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {'username': forms.TextInput(attrs={'class': 'log_f'}),
                   'email': forms.TextInput(attrs={'class': 'log_f'}),
                   'first_name': forms.TextInput(attrs={'class': 'log_f'}),
                   'last_name': forms.TextInput(attrs={'class': 'log_f'})}


__all__ = ['EditProfileForm']
