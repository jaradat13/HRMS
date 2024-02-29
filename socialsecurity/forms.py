from django import forms
from .models import EmployeeSSPercentage, CompanySSPercentage


class EmployeeSSPercentageForm(forms.ModelForm):
    class Meta:
        model = EmployeeSSPercentage
        fields = "__all__"
        labels = {
            'percentage': 'Employee Percentage',
        }


class CompanySSPercentageForm(forms.ModelForm):
    class Meta:
        model = CompanySSPercentage
        fields = "__all__"
        labels = {

            'percentage': 'Company Percentage'  # Change label for 'company_percentage' field
        }
