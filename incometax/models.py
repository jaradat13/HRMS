from decimal import Decimal

from django.db import models


class IncomeTaxPercentage(models.Model):
    name = models.CharField(max_length=100, unique=True, default='')
    percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return f"{self.name}-{self.percentage}"


class IncomeTaxDeductions(models.Model):
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    pay_period = models.ForeignKey('payroll.PayPeriod', on_delete=models.CASCADE)
    income_tax_deduction = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.pay_period}"
