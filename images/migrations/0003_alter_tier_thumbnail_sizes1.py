# Generated by Django 4.2.5 on 2023-09-22 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0002_auto_20230922_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tier',
            name='thumbnail_sizes1',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]