from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django_summernote.fields import SummernoteTextField
from ckeditor.fields import RichTextField


STATUS = ((0, "Draft"), (1, "Published"))

# Create your models here.


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
    A model to creat and manage handcrafts
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
    handcraft_type = models.CharField(
        max_length=50, choices=HANDCRAFT_TYPES, default="knitting"
    )

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"{self.title} | written by {self.author}"


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    body = models.TextField()
    approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_on"]

    def __str__(self):
        return f"Comment {self.body} by {self.author}"
