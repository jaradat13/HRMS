from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('', include('core.urls')),
                  path('', include('employee.urls')),
                  path('', include('allowance.urls')),
                  path('', include('incometax.urls')),
                  path('', include('socialsecurity.urls')),
                  path('', include('payroll.urls')),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
