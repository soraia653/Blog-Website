from socket import fromshare
from .models import Post

from django import forms

# create forms here
class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'body',)