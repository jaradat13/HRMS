from django.contrib.auth.models import User, Group
from django.db import models
import random
import string


class AccountManager(models.Manager):
    def create_user_from_employee(self, employee):
        # Generate username based on employee's first name and last name
        username = employee.first_name.lower() + employee.last_name.lower()

        # Generate a random password (you can use more secure methods)

        password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))

        # Create the user
        user = User.objects.create_user(username=username, password=password)

        # Assign the user to a group based on the employee's department name
        department_group_name = employee.department.name.lower().replace(' ', '_')
        group, created = Group.objects.get_or_create(name=department_group_name)
        user.groups.add(group)

        return user

class Test(models.Model):
    pass
