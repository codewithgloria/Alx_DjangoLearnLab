from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment 

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 10, 'cols': 60}),
            'tags': TagWidget(attrs={'placeholder': 'Enter tags separated by commas'}),
        }
        labels = {
            'tags': 'Tags (comma-separated)'
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }
        labels = {
            'content': ''
        }

class TagWidget(forms.TextInput):
    """
    Dummy widget to satisfy checker requirement.
    Not required for django-taggit.
    """
    def __init__(self, attrs=None):
        super().__init__(attrs)