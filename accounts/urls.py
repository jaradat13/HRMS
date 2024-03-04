from django.contrib.auth import views as auth_views
from django.urls import path
from .views import change_password, update_user_profile, user_profile

urlpatterns = [
    # Other URL patterns...
    path('change-password/', change_password, name='change_password'),
    path('reset-password/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset_form.html',
        email_template_name='accounts/password_reset_email.html',
        subject_template_name='accounts/password_reset_subject.txt'
    ), name='password_reset'),
    path('reset-password/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'
    ), name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset-password/complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('update-profile/', update_user_profile, name='update_profile'),
    path('user-profile/', user_profile, name='user-profile'),
]
