from django import forms
from django.forms import HiddenInput
from .models import Post, Comment


class Handcraftform(forms.ModelForm):
    """
    Form to create a handcraft post
    """

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "excerpt",
            "image",
            "image_alt",
            "handcraft_type",
            "status",  # Add status so you can publish directly
        ]

        widgets = {
            "slug": HiddenInput(),
            "content": forms.Textarea(attrs={"rows": 5}),
            "excerpt": forms.Textarea(attrs={"rows": 3}),
            "image_alt": forms.TextInput(attrs={
                "placeholder": "Describe your handcraft image (optional)"
            }),
        }

        labels = {
            "title": "Handcraft Title",
            "content": "Handcraft Story",
            "excerpt": "Story Teaser",
            "image": "Handcraft Image (Optional)",
            "image_alt": "Image Description",
            "handcraft_type": "Handcraft Type",
            "status": "Publication Status",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make these fields optional
        self.fields['image'].required = False
        self.fields['image_alt'].required = False
        self.fields['excerpt'].required = False

        # Add help text for the image field
        self.fields['image'].help_text = (
            "Leave empty to use default handcraft image"
            )

    def save(self, commit=True):
        instance = super().save(commit=False)

        # If no image is provided, the model's default will be used automatically
        # If no image_alt is provided, set a default based on the title
        if not instance.image_alt:
            instance.image_alt = f"{instance.title} - handcraft image"

        if commit:
            instance.save()
        return instance


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
