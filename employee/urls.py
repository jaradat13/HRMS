from django.urls import path

from payroll.views import search_employee_payroll_view
from . import views
from .views import ExportEmployeesExcelView, import_employees

urlpatterns = [
    path('employees/', views.employee_list_view, name='employee-list'),
    path('employees/<int:pk>/', views.employee_detail_view, name='employee-detail'),
    path('employees/create/', views.employee_create_view, name='employee-create'),
    path('employees/<int:pk>/update/', views.employee_update_view, name='employee-update'),
    path('employees/<int:pk>/delete/', views.employee_delete_view, name='employee-delete'),
    path('employee_search/', views.employee_search, name='employee_search'),
    path('export-employees-excel/', ExportEmployeesExcelView.as_view(), name='export_employees_excel'),
    path('import/', import_employees, name='employee-import'),
    path('search/', search_employee_payroll_view, name='search_employee_payroll'),
]
