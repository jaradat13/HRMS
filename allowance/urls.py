from django.urls import path
from . import views
from .views import allowance_payments_view

urlpatterns = [
    path('allowance/', views.allowance_list, name='allowance_list'),
    path('mobile-allowance/create/', views.mobile_allowance_create, name='mobile_allowance_create'),
    path('mobile-allowance/<int:pk>/update/', views.mobile_allowance_update, name='mobile_allowance_update'),
    path('mobile-allowance/<int:pk>/delete/', views.mobile_allowance_delete, name='mobile_allowance_delete'),
    path('travel-allowance/create/', views.travel_allowance_create, name='travel_allowance_create'),
    path('travel-allowance/<int:pk>/update/', views.travel_allowance_update, name='travel_allowance_update'),
    path('trave-allowance/<int:pk>/delete/', views.travel_allowance_delete, name='travel_allowance_delete'),
    path('medical-allowance/create/', views.medical_allowance_create, name='medical_allowance_create'),
    path('medical-allowance/<int:pk>/update/', views.medical_allowance_update, name='medical_allowance_update'),
    path('medical-allowance/<int:pk>/delete/', views.medical_allowance_delete, name='medical_allowance_delete'),
    path('housing-allowance/create/', views.housing_allowance_create, name='housing_allowance_create'),
    path('housing-allowance/<int:pk>/update/', views.housing_allowance_update, name='housing_allowance_update'),
    path('housing-allowance/<int:pk>/delete/', views.housing_allowance_delete, name='housing_allowance_delete'),
    path('uniform-allowance/create/', views.uniform_allowance_create, name='uniform_allowance_create'),
    path('uniform-allowance/<int:pk>/update/', views.uniform_allowance_update, name='uniform_allowance_update'),
    path('uniform-allowance/<int:pk>/delete/', views.uniform_allowance_delete, name='uniform_allowance_delete'),
    path('other-allowance/create/', views.other_allowance_create, name='other_allowance_create'),
    path('other-allowance/<int:pk>/update/', views.other_allowance_update, name='other_allowance_update'),
    path('other-allowance/<int:pk>/delete/', views.other_allowance_delete, name='other_allowance_delete'),
    path('allowance-payments/', allowance_payments_view, name='allowance_payments'),
]
