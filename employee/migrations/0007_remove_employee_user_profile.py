# Generated by Django 5.0.2 on 2024-03-04 11:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0006_alter_employee_user_profile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employee',
            name='user_profile',
        ),
    ]
