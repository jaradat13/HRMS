from django import forms
from .models import Company, Department, Section, JobTitle


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = '__all__'


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = '__all__'


class SectionForm(forms.ModelForm):
    class Meta:
        model = Section
        fields = '__all__'


class JobTitleForm(forms.ModelForm):
    class Meta:
        model = JobTitle
        fields = '__all__'
