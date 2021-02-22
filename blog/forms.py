from django import forms
from .models import Post, Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'body', 'slug', 'status')

class CommentForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label='Comment')
