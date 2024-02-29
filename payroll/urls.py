from django.urls import path
from . import views
from .views import generate_payroll, close_payroll_period, ExportPayrollExcelView

urlpatterns = [
    path('pay-periods/', views.pay_period_list_view, name='pay-period-list'),
    path('pay-periods/<int:pk>/', views.pay_period_detail_view, name='pay-period-detail'),
    path('pay-periods/create/', views.pay_period_create_view, name='pay-period-create'),
    path('pay-periods/<int:pk>/update/', views.pay_period_update_view, name='pay-period-update'),
    path('pay-periods/<int:pk>/delete/', views.pay_period_delete_view, name='pay-period-delete'),
    path('payrolls/<int:pk>/', views.payroll_detail_view, name='payroll-detail'),
    path('payrolls/create/', views.payroll_create_view, name='payroll-create'),
    path('payrolls/<str:month>/<int:year>/', views.payroll_list_view, name='payroll-list'),
    path('payrolls/<int:pk>/update/', views.payroll_update_view, name='payroll-update'),
    path('payrolls/<int:pk>/delete/', views.payroll_delete_view, name='payroll-delete'),
    path('generate-payroll/', generate_payroll, name='generate_payroll'),
    path('close-payroll-period/<int:period_id>/', close_payroll_period, name='close_payroll_period'),
    path('export-payroll-excel/<int:pay_period_id>/', ExportPayrollExcelView.as_view(), name='export_payroll_excel'),

]
