# Generated by Django 5.0.2 on 2024-03-04 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_alter_userprofile_user'),
        ('employee', '0007_remove_employee_user_profile'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]