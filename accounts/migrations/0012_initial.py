# Generated by Django 5.0.2 on 2024-03-04 11:30

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0011_delete_userprofile'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=25)),
                ('second_name', models.CharField(blank=True, max_length=25, null=True)),
                ('last_name', models.CharField(blank=True, max_length=25, null=True)),
                ('phone_number', models.CharField(max_length=18)),
                ('address', models.CharField(blank=True, max_length=100, null=True)),
                ('emergency_contact_name', models.CharField(blank=True, default=None, max_length=100)),
                ('emergency_contact_phone', models.CharField(blank=True, max_length=18, null=True)),
                ('number_of_dependents', models.PositiveIntegerField(blank=True, default=0, null=True)),
                ('bank_name', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_branch', models.CharField(blank=True, max_length=100, null=True)),
                ('bank_account_number', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'User Profile',
                'verbose_name_plural': 'User Profiles',
            },
        ),
    ]