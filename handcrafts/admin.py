from django.contrib import admin
from .models import Post, Comment


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author', 'body', 'created_on', 'approved', 'post')
    lis_filter = ('approved', 'created_on')
    search_fields = ('author_username', 'body')
    actions = ['approve_comments']

    def approve_comments(self, request, queryset):
        queryset.update(approved=True)
        self.message_user(request, 'Comments approved')
