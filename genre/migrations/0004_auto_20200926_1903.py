# Generated by Django 3.0.2 on 2020-09-26 16:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('genre', '0003_remove_genre_timestamp'),
    ]

    operations = [
        migrations.RenameField(
            model_name='genre',
            old_name='url',
            new_name='slug',
        ),
    ]
