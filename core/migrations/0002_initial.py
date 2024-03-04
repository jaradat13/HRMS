# Generated by Django 5.0.2 on 2024-03-02 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0001_initial'),
        ('employee', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='head',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department_head', to='employee.employee'),
        ),
        migrations.AddField(
            model_name='jobtitle',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='job_titles', to='core.department'),
        ),
        migrations.AddField(
            model_name='section',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='core.department'),
        ),
        migrations.AddField(
            model_name='jobtitle',
            name='section',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_titles', to='core.section'),
        ),
    ]
