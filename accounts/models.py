from django.core.mail import send_mail
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class AccountManager(models.Manager):
    def create_user_from_employee(self, employee):
        # Generate username based on employee's first name and last name
        username = employee.first_name.lower() + employee.last_name.lower()

        # Generate a random password (you can use more secure methods)
        import random
        import string
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        # Assign the user to a group based on the employee's department name
        department_group_name = employee.department.name.lower().replace(' ', '_')
        group, created = Group.objects.get_or_create(name=department_group_name)
        user.groups.add(group)

        # Send email notification
        subject = 'Your Account Details'
        message = f'Your username is {username} and your password is {password}.'
        sender_email = settings.EMAIL_HOST_USER
        recipient_email = employee.email
        send_mail(subject, message, sender_email, [recipient_email])
        if not hasattr(user, 'userprofile'):
            UserProfile.objects.create(user=user, phone_number=employee.phone_number)

        return user


class UserProfile(models.Model):
    employee = models.ForeignKey("employee.Employee", on_delete=models.CASCADE, default=None)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(default=None, blank=True, null=True)

    # Add more fields as needed (e.g., address, profile picture, etc.)

    def __str__(self):
        return str(self.user)
