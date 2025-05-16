from django.contrib import admin
from .models import Post, Comment

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'handcraft_type',
        'author',
    )
    list_filter = ('handcraft_type')
