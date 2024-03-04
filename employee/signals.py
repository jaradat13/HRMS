from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import UserProfile
from employee.models import Employee


@receiver(post_save, sender=Employee)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        username = f"{instance.first_name}.{instance.last_name}".lower()
        # Create a new user
        user = User.objects.create_user(
            username=username,
            email=instance.email,
            password=str(instance.employee_id),  # Use employee ID as password
            first_name=instance.first_name,
            last_name=instance.last_name
        )

        # Create a UserProfile instance
        profile = UserProfile.objects.create(
            user=user,
            first_name=instance.first_name,
            second_name=instance.second_name,
            last_name=instance.last_name,
            phone_number = instance.phone_number,
            address = instance.address,
            emergency_contact_name = instance.emergency_contact_name,
            emergency_contact_phone = instance.emergency_contact_phone,
            number_of_dependents = instance.number_of_dependents,
            bank_name = instance.bank_name,
            bank_branch = instance.bank_branch,
            bank_account_number = instance.bank_account_number,
            # Copy other relevant fields from the Employee instance
        )

        # Assign the employee to a group based on department name
        department_group_name = instance.department.name
        group, created = Group.objects.get_or_create(name=department_group_name)
        group.user_set.add(user)
