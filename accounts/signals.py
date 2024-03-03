from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from accounts.models import UserProfile
from employee.models import Employee


@receiver(post_save, sender=Employee)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Check if the user has an associated employee
        try:
            employee = Employee.objects.get(email=instance.email)
            # If an associated employee is found, create a UserProfile instance
            UserProfile.objects.create(employee=employee, user=instance)
        except Employee.DoesNotExist:
            pass
