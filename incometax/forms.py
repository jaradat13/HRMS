from django import forms
from .models import IncomeTaxPercentage

class IncomeTaxPercentageForm(forms.ModelForm):
    class Meta:
        model = IncomeTaxPercentage
        fields = '__all__'
