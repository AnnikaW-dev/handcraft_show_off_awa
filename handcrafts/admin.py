from django.contrib import admin
from .models import Post, Comment
from django_summernote.admin import SummernoteInlineModelAdmin


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "handcraft_type",
        "author",
    )
    list_filter = "handcraft_type"
    search_fields = ["title"]
    list_filter = ("status",)
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ("content", "excerpt")


# Register your models here.
admin.site.register(Comment)
