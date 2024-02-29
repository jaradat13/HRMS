from django.urls import path
from . import views
from .views import IncomeTaxDeductionsExport

urlpatterns = [
    path('income-tax-percentages/', views.income_tax_percentage_list_view, name='income-tax-percentage-list'),
    path('income-tax-percentages/<int:pk>/', views.income_tax_percentage_detail_view,
         name='income-tax-percentage-detail'),
    path('income-tax-percentages/create/', views.income_tax_percentage_create_view,
         name='income-tax-percentage-create'),
    path('income-tax-percentages/<int:pk>/update/', views.income_tax_percentage_update_view,
         name='income-tax-percentage-update'),
    path('income-tax-percentages/<int:pk>/delete/', views.income_tax_percentage_delete_view,
         name='income-tax-percentage-delete'),
    path('income-tax-deductions/<int:pay_period_id>/', IncomeTaxDeductionsExport.as_view(),
         name='income-tax-deductions'),
]
