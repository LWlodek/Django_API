# Generated by Django 4.2.5 on 2023-09-24 18:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_remove_image_thumbnail_image_thumbnail_200px_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(default='default_thumbnail.jpg', upload_to='thumbnails/'),
        ),
    ]
