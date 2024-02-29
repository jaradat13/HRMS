from django.contrib import admin
from .models import (MobileAllowance, TravelAllowance, HousingAllowance, UniformAllowance, OtherAllowance,
                     MedicalAllowance, AllowancePayments)

admin.site.register(MobileAllowance)
admin.site.register(TravelAllowance)
admin.site.register(HousingAllowance)
admin.site.register(UniformAllowance)
admin.site.register(OtherAllowance)
admin.site.register(MedicalAllowance)
admin.site.register(AllowancePayments)
