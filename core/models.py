from auditlog.registry import auditlog
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from employee.models import Employee


class Company(models.Model):
    """
    A company model that stores information about a company.

    Attributes:
        name (CharField): The name of the company.
        phone (CharField): The phone number of the company.
        email (EmailField): The email of the company.
        website (CharField): The website of the company.
        address (CharField): The address of the company.
        country (CharField): The country of the company.
        logo (ImageField): The logo of the company.
        icon (ImageField): The icon of the company.

    Methods:
        __str__(self): Returns the name of the company.
    """
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
    """
    A model that represents a department in an organization.

    Attributes:
        name (CharField): The name of the department.

    Methods:
        __str__(self): Returns the name of the department.
    """
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
    """
    A model that represents a section in an organization.

    Attributes:
        name (CharField): The name of the section.
        department (ForeignKey): The department that the section belongs to.

    Methods:
        __str__(self): Returns the name of the section.
    """
    name = models.CharField(max_length=100)
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name='sections'
    )

    def __str__(self):
        return self.name


class JobTitle(models.Model):
    """
    A model that represents a job title in an organization.

    Attributes:
        name (CharField): The name of the job title.
        department (ForeignKey): The department that the job title belongs to.
        section (ForeignKey): The section that the job title belongs to.
        description (CharField): A description of the job title.

    Methods:
        __str__(self): Returns the name of the job title.
    """
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
