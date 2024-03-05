from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import UserProfile, Employee

@receiver(post_save, sender=UserProfile)
def update_employee_profile(sender, instance, created, **kwargs):
    """
    Signal receiver function to update the corresponding Employee model
    whenever a UserProfile instance is created or updated.
    """
    if created:
        # If a new UserProfile instance is created, create a corresponding Employee instance
        Employee.objects.create(user=instance.user)  # Add necessary fields initialization
    else:
        # If an existing UserProfile instance is updated, update the corresponding Employee instance
        employee = Employee.objects.get(user=instance.user)
        employee.second_name = instance.second_name  # Update fields as needed
        employee.phone_number = instance.phone_number # Update fields as needed
        employee.image_url = instance.image.url # Update fields as needed
        # Save the Employee instance
        employee.save()
