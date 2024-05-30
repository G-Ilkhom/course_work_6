from django import forms
from blog.models import BlogPost
from mailings.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = 'title', 'content', 'image'
