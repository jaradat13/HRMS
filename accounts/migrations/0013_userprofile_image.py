# Generated by Django 5.0.2 on 2024-03-04 15:58

import accounts.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0012_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='image',
            field=models.ImageField(blank=True, default='default.jpg', null=True, upload_to='media/employees_images/', validators=[accounts.models.validate_image_size]),
        ),
    ]