from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import models
from django.forms import ValidationError

from .models import Community, Comment


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )


class PostCreateForm(forms.Form):
    title = forms.CharField(label='Title', max_length=50)
    content = forms.CharField(label='Content', required=False, widget=forms.Textarea)
    community = forms.SlugField(label='Community', required=True)

    def clean_community(self):
        community = self.cleaned_data['community']
        if not Community.objects.filter(slug=community).exists():
            raise ValidationError("Community doesn't exist")
        return community


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('uploader', 'content', )


