from django import forms
from .models import Comment, Post


class SearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'class': "form_e", 'placeholder': 'Search'}))


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


__all__ = ['EditPostForm', 'AddPostForm', 'SearchForm']
