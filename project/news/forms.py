from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    # description = forms.CharField(min_length=20)

    class Meta:
        model = Post
        fields = ['titl', 'post_category', 'text', 'author']
