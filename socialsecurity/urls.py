from django.urls import path
from . import views
from .views import calculate_and_show_ss_deductions, ExportSocialSecurityDeductionsView, edit_ss_percentage

urlpatterns = [
    path('set/', views.set_ss_percentage, name='set_ss_percentage'),  # URL for setting new percentage values
    path('edit-ss-percentage/<int:employee_id>/<int:company_id>/', views.edit_ss_percentage, name='edit_ss_percentage'),
    path('list/', views.list_ss_percentages, name='list_ss_percentages'),  # URL for listing all percentage values
    path('calculate-ss-deductions/<int:pay_period_id>/', calculate_and_show_ss_deductions,
         name='calculate_ss_deductions'),
    path('export-ss_deductions-excel/<int:pay_period_id>/', ExportSocialSecurityDeductionsView.as_view(),
         name='export-ss_deductions-excel'),

]
