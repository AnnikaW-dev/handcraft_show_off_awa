from django import forms
from .models import Post


class Handcraftform(forms.ModelForm):
    """
    Form to creat a handcraft post
    """

    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "content",
            "excerpt",
            "image",
            "handcraft_type",
            "image",
        ]

        labels = {
            "title": "Handcraft Title",
            "content": "Handcraft Story",
            "excerpt": "Story Teaser",
            "image": "Handcraft Image",
            "handcraft_type": "Handcraft Type",
        }
