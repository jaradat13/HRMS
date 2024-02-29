from django.contrib import admin
from .models import Company, Department, Section, JobTitle

admin.site.register(Company)
admin.site.register(Department)
admin.site.register(Section)
admin.site.register(JobTitle)
