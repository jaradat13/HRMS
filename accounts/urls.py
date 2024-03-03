from django.urls import path
from accounts.views import update_profile

urlpatterns = [
    path('profile/update/', update_profile, name='update_profile'),
    # Add more URL patterns as needed
]