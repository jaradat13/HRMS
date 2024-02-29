from django.contrib import admin
from .models import Employee
from simple_history.admin import SimpleHistoryAdmin

admin.site.register(Employee,SimpleHistoryAdmin)
