from auditlog.registry import auditlog
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from employee.models import Employee


class Company(models.Model):
    name = models.CharField(max_length=50, default='')
    phone = models.CharField(max_length=50, default='')
    email = models.EmailField(default='')
    website = models.CharField(max_length=50, default='')
    address = models.CharField(max_length=100, default='')
    country = models.CharField(max_length=50, default='')
    logo = models.ImageField(upload_to='media/company-logo/')
    icon = models.ImageField(upload_to='media/company-icon/')

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    head = models.OneToOneField(
        'employee.Employee',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='department_head'
    )

    def __str__(self):
        return self.name


class Section(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='sections'
    )

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='job_titles'
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='job_titles'
    )
    description = models.CharField(max_length=100, default='', blank=True, null=True)

    def __str__(self):
        return self.name





auditlog.register(Company)
auditlog.register(Department)
auditlog.register(Section)
auditlog.register(JobTitle)
