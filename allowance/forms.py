from django import forms
from .models import MobileAllowance, TravelAllowance, HousingAllowance, UniformAllowance, MedicalAllowance, \
    OtherAllowance


class MobileAllowanceForm(forms.ModelForm):
    class Meta:
        model = MobileAllowance
        fields = ['amount']


class TravelAllowanceForm(forms.ModelForm):
    class Meta:
        model = TravelAllowance
        fields = ['amount']


class HousingAllowanceForm(forms.ModelForm):
    class Meta:
        model = HousingAllowance
        fields = ['amount']


class UniformAllowanceForm(forms.ModelForm):
    class Meta:
        model = UniformAllowance
        fields = ['amount']


class MedicalAllowanceForm(forms.ModelForm):
    class Meta:
        model = MedicalAllowance
        fields = ['amount']


class OtherAllowanceForm(forms.ModelForm):
    class Meta:
        model = OtherAllowance
        fields = ['amount']
