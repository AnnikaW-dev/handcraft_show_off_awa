from django.db import models
from django.contrib.auth.models import User
from django_summernote.fields import SummernoteTextField
from django.core.files.base import ContentFile

from cloudinary.models import CloudinaryField
from ckeditor.fields import RichTextField
from PIL import Image
import io
import cloudinary.uploader



STATUS = ((0, "Draft"), (1, "Published"))


# Choise Fields
HANDCRAFT_TYPES = (
    ("knitting", "Knitting"),
    ("crochet", "Crochet"),
    ("sewing", "sewing"),
    ("embroodery", "Embroidery"),
    ("other", "Other"),
)


class Post(models.Model):
    """
    A model to create and manage handcrafts
    """
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="handcraft_posts"
    )
    content = RichTextField()
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    excerpt = RichTextField(blank=True)
    updated_on = models.DateTimeField(auto_now=True)
    image = CloudinaryField("image", default="placeholder")
    thumbnail = CloudinaryField("thumbnail", blank=True, null=True)
    image_alt = models.CharField(max_length=200, blank=False)
    handcraft_type = models.CharField(
        max_length=50, choices=HANDCRAFT_TYPES, default="knitting"
    )

    class Meta:
        ordering = ["-created_on"]

    def save(self, *args, **kwargs):
        """
        Only create thumbnails if image exists and not the default placeholder
        """
        if self.image and str(self.image) != "placeholder":
            try:
                image_url = self.image.url
                # Create thumbnail using Cloudinary's transformation
                # This creates a 286x386 thumbnail with smart cropping
                thumbnail_url = cloudinary.CloudinaryImage(str(self.image)).build_url(
                    width=286,
                    height=382,
                    crop="fill",  # This maintans the ratio and corp if needed
                    quality="auto",
                    fetch_format="auto",
                )

                # Store the thumbnail reference
                self.thumbnail = str(self.image)
            except Exception as e:
                print(f"Error creating thumbnail: {e}")

        super().save(*args, **kwargs)
    def get_thumbnail_url(self):
        """
        Get the thumbnail URL with Cloudinary transformations
        """
        if self.image and str(self.image) != "placeholder":
            return cloudinary.CloudinaryImage(str(self.image)).build_url(
                width=286,
                    height=382,
                    crop="fill",
                    quality="auto",
                    fetch_format="auto"
            )
        return None

    def get_detail_image_url(self):
        """
        Get the full-size image URL for detail view
        """
        if self.image and str(self.image) != "placeholder":
            return cloudinary.CloudinaryImage(str(self.image)).build_url(
                width=800, #Max width for detail
                quality="auto",
                fetch_format="auto"
            )
        return self.image.url if self.image else None

    def __str__(self):
        return f"{self.title} | written by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
        )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="commenter"
        )
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='favorited_by')
    create_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"{self.user.username} favorited {self.ppost.title}"
