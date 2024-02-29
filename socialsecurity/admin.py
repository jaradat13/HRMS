from django.contrib import admin
from .models import EmployeeSSPercentage, CompanySSPercentage, SocialSecurityDeductions

admin.site.register(EmployeeSSPercentage)
admin.site.register(CompanySSPercentage)
admin.site.register(SocialSecurityDeductions)
