from django import forms
from .models import Comment, Post
from django.forms.widgets import Input
from datetime import datetime


class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
        widgets = {
            'title': Input(attrs={'class': "form-control", 'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'class': "form-control", 'placeholder': 'Write Text for Post...'}),
        }

    def save(self, commit=True):
        post = super().save(commit=False)
        # there cannot pass user and write 1 for user pk.
        # post.author = User.objects.get(pk=1)
        post.created = datetime.now()
        if commit:
            post.save()
        return post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # fields = '__all__'
        fields = ['text']
