from tkinter import Widget
from django import forms
from .models import Post
from django.forms.widgets import Input




class PostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image']
        widgets = {
            'title': Input(attrs={'class':"form-control", 'placeholder': 'Title'}),
            'text': forms.Textarea(attrs={'class':"form-control"}),
        }