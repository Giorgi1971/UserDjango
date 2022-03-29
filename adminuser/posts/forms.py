from django import forms
from .models import Comment, Post
from django.forms.widgets import Input
from datetime import datetime
from django.contrib.auth.models import User


class PostModelForm(forms.ModelForm):
    
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
        widgets = {
            'title': Input(attrs={'class':"form-control", 'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'class':"form-control", 'placeholder': 'Teext'}),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        # აქ ვერ ვაწვდი უზერს და მიწერია 1 ანუ ადმინის pk.
        # post.author = User.objects.get(pk=1)
        post.created = datetime.now()
        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
