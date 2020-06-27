from django import forms
from .models import Post, Comment
from django.forms import ModelForm, TextInput
from .models import City


class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ('author','title','subtitle','text', 'pic','video')

    widgets = {
        'title': forms.Textarea(attrs={'class':'textinputclass'}),
        'text': forms.Textarea(attrs={'class':'editable medium-editor-textarea postcontent'}),
    }


class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

    widgets = {
        'author': forms.TextInput(attrs={'class': 'textinputclass'}),
        'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
    }


class CityForm(ModelForm):
    class Meta:
        model = City
        fields = ['city']
        widgets = {'city' : TextInput(attrs={'class' : 'input', 'placeholder' : 'City Name'})}
