from django import forms
from django.forms import HiddenInput
from .models import Post, Comment


class Handcraftform(forms.ModelForm):
    """
    Form to creat a handcraft post
    """

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "excerpt",
            "image",
            "handcraft_type",
            "image",
        ]

        widgets = {
            "slug": HiddenInput(),
        }

        labels = {
            "title": "Handcraft Title",
            "content": "Handcraft Story",
            "excerpt": "Story Teaser",
            "image": "Handcraft Image",
            "handcraft_type": "Handcraft Type",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        labels = {
            'body': 'Comment'
        }
        widgets = {
            'body': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Add your comment here...'
            }),
        }
