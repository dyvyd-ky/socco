# Generated by Django 4.1.3 on 2022-11-26 10:37

import ckeditor_uploader.fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("product", "0002_alter_category_image"),
    ]

    operations = [
        migrations.AddField(
            model_name="category",
            name="display",
            field=ckeditor_uploader.fields.RichTextUploadingField(
                default=django.utils.timezone.now
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="category",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="uploads/"),
        ),
    ]
