from django import forms
from chat.models import Message


class ChatForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['body']
        widgets = {'body': forms.TextInput(attrs={'class': "form_msg", 'placeholder': 'Type'})}


__all__ = ['ChatForm']
