from django import forms
from accounts.models import User


class EditProfilePersonalForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']
        widgets = {'username': forms.TextInput(attrs={'class': 'text_field'}),
                   'first_name': forms.TextInput(attrs={'class': 'text_field'}),
                   'last_name': forms.TextInput(attrs={'class': 'text_field'})}


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['image', 'bio', 'gender', 'website']
        widgets = {'image': forms.FileInput(attrs={'class': 'img_upload', 'id': 'prof_img'}),
                   'website': forms.TextInput(attrs={'class': 'text_field'}),
                   'bio': forms.Textarea(attrs={'class': 'bio', 'rows': 7}),
                   'gender': forms.TextInput(attrs={'class': 'text_field', 'readonly': True})}


class EditSecurityForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']
        widgets = {'password': forms.TextInput(attrs={'class': 'text_field'})}


class EditNotificationsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']
        widgets = {'email': forms.TextInput(attrs={'class': 'text_field'})}


__all__ = ['EditProfileForm', 'EditProfilePersonalForm', 'EditNotificationsForm', 'EditSecurityForm']
