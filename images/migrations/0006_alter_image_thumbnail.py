# Generated by Django 4.2.5 on 2023-09-24 11:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0005_rename_thumbnail_sizes1_tier_thumbnail_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='thumbnail',
            field=models.ImageField(upload_to='thumbnails/'),
        ),
    ]
