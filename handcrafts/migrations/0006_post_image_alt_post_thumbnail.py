# Generated by Django 5.2 on 2025-05-27 11:57

import cloudinary.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("handcrafts", "0005_alter_post_content_alter_post_excerpt"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="image_alt",
            field=models.CharField(default="Handcraft image", max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="post",
            name="thumbnail",
            field=cloudinary.models.CloudinaryField(
                blank=True, max_length=255, null=True, verbose_name="thumbnail"
            ),
        ),
    ]
