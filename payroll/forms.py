from django import forms
from .models import PayPeriod, Payroll


class PayPeriodForm(forms.ModelForm):
    class Meta:
        model = PayPeriod
        exclude = ('start_date', 'end_date', 'is_closed')


class PayrollForm(forms.ModelForm):
    class Meta:
        model = Payroll
        fields = '__all__'
