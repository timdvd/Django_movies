# Generated by Django 3.0.2 on 2020-09-25 15:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('category', '0002_auto_20200925_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(blank=True, default='', max_length=100, null=True, unique=True),
        ),
    ]
