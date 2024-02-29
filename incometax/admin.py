from django.contrib import admin
from .models import IncomeTaxPercentage, IncomeTaxDeductions

admin.site.register(IncomeTaxPercentage)
admin.site.register(IncomeTaxDeductions)
