from calendar import monthrange
from decimal import Decimal

from auditlog.registry import auditlog
from django.db import models
from django.utils import timezone

from allowance.models import MobileAllowance, TravelAllowance, HousingAllowance, OtherAllowance, UniformAllowance
from incometax.models import IncomeTaxPercentage
from socialsecurity.models import EmployeeSSPercentage, CompanySSPercentage


class PayPeriod(models.Model):
    MONTH_CHOICES = [
        ('January', 'January'),
        ('February', 'February'),
        ('March', 'March'),
        ('April', 'April'),
        ('May', 'May'),
        ('June', 'June'),
        ('July', 'July'),
        ('August', 'August'),
        ('September', 'September'),
        ('October', 'October'),
        ('November', 'November'),
        ('December', 'December'),
    ]

    month = models.CharField(max_length=20, choices=MONTH_CHOICES, default=timezone.now().strftime('%B'))
    year = models.IntegerField(default=timezone.now().year)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    is_closed = models.BooleanField(default=False)

    class Meta:
        unique_together = [['month', 'year']]

    def save(self, *args, **kwargs):
        # Parse the month string into its corresponding index in MONTH_CHOICES
        month_index = [month[0] for month in self.MONTH_CHOICES].index(self.month) + 1

        # Set start_date to the first day of the selected month
        start_day = timezone.datetime(self.year, month_index, 1).date()
        # Set end_date to the last day of the selected month
        _, last_day = monthrange(self.year, month_index)
        end_day = timezone.datetime(self.year, month_index, last_day).date()

        self.start_date = start_day
        self.end_date = end_day

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.month} {self.year}"



class Payroll(models.Model):
    pay_period = models.ForeignKey(PayPeriod, on_delete=models.CASCADE)
    employee = models.ForeignKey('employee.Employee', on_delete=models.CASCADE, related_name='employee_payroll')
    basic_salary = models.DecimalField(decimal_places=2, default=None, max_digits=10)
    gross_salary = models.DecimalField(decimal_places=2, default=None, max_digits=10)
    net_salary = models.DecimalField(decimal_places=2, default=None, max_digits=10)
    mobile_allowance = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    travel_allowance = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    housing_allowance = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    medical_allowance = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    uniform_allowance = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    other_allowance = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    total_allowance = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    employee_ss_deduction = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    company_ss_deduction = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    income_tax_deduction = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    other_deductions = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    employee_total_deduction = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)
    total_deductions = models.DecimalField(decimal_places=2, default=None, max_digits=10, null=True)

    def __str__(self):
        return f"{self.pay_period} - {self.employee}"


auditlog.register(PayPeriod)
auditlog.register(Payroll)