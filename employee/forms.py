from django import forms
from django.contrib import admin
from .models import Employee
from allowance.models import MobileAllowance, TravelAllowance, HousingAllowance, MedicalAllowance, OtherAllowance


class EmployeeForm(forms.ModelForm):

    class Meta:
        model = Employee
        exclude = ('payroll', 'is_active', 'created_by','edited_by')

class EmployeeImportForm(forms.Form):
    file = forms.FileField()


