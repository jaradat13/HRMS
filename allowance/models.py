from decimal import Decimal
from django.db import models
from auditlog.registry import auditlog



class Allowance(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True, blank=True, unique=True)

    class Meta:
        abstract = True


class MobileAllowance(Allowance):
    def __str__(self):
        return f"Mobile Allowance: {self.amount}"


class TravelAllowance(Allowance):
    def __str__(self):
        return f"Travel Allowance: {self.amount}"


class HousingAllowance(Allowance):
    def __str__(self):
        return f"Housing Allowance: {self.amount}"


class UniformAllowance(Allowance):
    def __str__(self):
        return f"Uniform Allowance: {self.amount}"


class MedicalAllowance(Allowance):
    def __str__(self):
        return f"Medical Allowance: {self.amount}"


class OtherAllowance(Allowance):
    def __str__(self):
        return f"Other Allowance: {self.amount}"


class AllowancePayments(models.Model):
    employee = models.ForeignKey('employee.Employee', on_delete=models.SET_NULL,null=True)
    pay_period = models.ForeignKey('payroll.PayPeriod', on_delete=models.CASCADE, null=True)
    mobile_allowance_payment = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)
    travel_allowance_payment = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)
    housing_allowance_payment = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)
    medical_allowance_payment = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)
    uniform_allowance_payment = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)
    other_allowance_payment = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)
    total_allowance_payment = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.pay_period}"


auditlog.register(MobileAllowance)
auditlog.register(TravelAllowance)
auditlog.register(HousingAllowance)
auditlog.register(MedicalAllowance)
auditlog.register(UniformAllowance)
auditlog.register(OtherAllowance)
