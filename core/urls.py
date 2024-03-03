from django.urls import path, include
from . import views
from .views import login_view, logout_view

urlpatterns = [
    path('', views.home, name='home'),

    # URLs for Company
    path('company/', views.company_list_view, name='company-list'),
    path('company/<int:pk>/', views.company_detail_view, name='company-detail'),
    path('company/create/', views.company_create_view, name='company-create'),
    path('company/<int:pk>/update/', views.company_update_view, name='company-update'),
    path('company/<int:pk>/delete/', views.company_delete_view, name='company-delete'),

    # URLs for Department

    path('department/', views.department_list_view, name='department-list'),
    path('department/<int:pk>/', views.department_detail_view, name='department-detail'),
    path('department/create/', views.department_create_view, name='department-create'),
    path('department/<int:pk>/update/', views.department_update_view, name='department-update'),
    path('department/<int:pk>/delete/', views.department_delete_view, name='department-delete'),
    path('export_department_employees_to_excel/<int:department_id>/', views.export_department_employees_to_excel, name='export_department_employees_to_excel'),

    # URLs for Section

    path('section/', views.section_list_view, name='section-list'),
    path('section/<int:pk>/', views.section_detail_view, name='section-detail'),
    path('section/create/', views.section_create_view, name='section-create'),
    path('section/<int:pk>/update/', views.section_update_view, name='section-update'),
    path('section/<int:pk>/delete/', views.section_delete_view, name='section-delete'),

    # URLs for JobTitle

    path('jobtitle/', views.jobtitle_list_view, name='jobtitle-list'),
    path('jobtitle/<int:pk>/', views.jobtitle_detail_view, name='jobtitle-detail'),
    path('jobtitle/create/', views.jobtitle_create_view, name='jobtitle-create'),
    path('jobtitle/<int:pk>/update/', views.jobtitle_update_view, name='jobtitle-update'),
    path('jobtitle/<int:pk>/delete/', views.jobtitle_delete_view, name='jobtitle-delete'),

    path('accounts/', include('django.contrib.auth.urls')),  # Include Django's built-in auth URLs for password reset
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]
