# Generated by Django 3.0.2 on 2020-09-26 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('actors', '0002_auto_20200926_1346'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='actor',
            name='timestamp',
        ),
    ]
