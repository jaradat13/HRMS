from decimal import Decimal

from auditlog.registry import auditlog
from django.db import models


class EmployeeSSPercentage(models.Model):
    percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.percentage)


class CompanySSPercentage(models.Model):
    percentage = models.DecimalField(max_digits=4, decimal_places=2, default=0, blank=True, null=True)

    def __str__(self):
        return str(self.percentage)


class SocialSecurityDeductions(models.Model):
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE)
    pay_period = models.ForeignKey('payroll.PayPeriod', on_delete=models.CASCADE)
    employee_ss_deduction = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)
    company_ss_deduction = models.DecimalField(decimal_places=2, default=Decimal('0'), max_digits=10)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.pay_period}"


auditlog.register(EmployeeSSPercentage)
auditlog.register(CompanySSPercentage)
auditlog.register(SocialSecurityDeductions)