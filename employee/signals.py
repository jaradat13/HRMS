from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Employee


@receiver(post_save, sender=Employee)
def create_or_update_user(sender, instance, created, **kwargs):
    if created:
        # Generate a unique username based on email
        username = instance.email
        # Create a new user
        user = User.objects.create_user(username=username, password=str(instance.employee_id))
        user.first_name = instance.first_name
        user.last_name = instance.last_name
        user.email = instance.email
        user.save()


@receiver(pre_delete, sender=Employee)
def delete_user(sender, instance, **kwargs):
    # Delete the associated user
    try:
        user = User.objects.get(username=instance.email)
        user.delete()
    except User.DoesNotExist:
        pass
