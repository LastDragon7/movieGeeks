# Generated by Django 4.2.16 on 2024-10-13 06:42

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ratings', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Ratings',
            new_name='Rating',
        ),
    ]
