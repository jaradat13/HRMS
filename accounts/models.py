from django.contrib.auth.models import User
from django.db import models
from employee.models import Employee  # Assuming your Employee model is in employee.models


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=25)
    second_name = models.CharField(max_length=25, blank=True, null=True)
    last_name = models.CharField(max_length=25, blank=True, null=True)
    phone_number = models.CharField(max_length=18)
    address = models.CharField(max_length=100, blank=True, null=True)
    emergency_contact_name = models.CharField(max_length=100, default=None, blank=True)
    emergency_contact_phone = models.CharField(max_length=18, blank=True, null=True)
    number_of_dependents = models.PositiveIntegerField(default=0, blank=True, null=True)
    bank_name = models.CharField(max_length=100, blank=True, null=True)
    bank_branch = models.CharField(max_length=100, blank=True, null=True)
    bank_account_number = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"
