from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls import (
#     handler400, handler403, handler404, handler500
# )

handler404 = 'Home.views.handler404'
handler500 = 'Home.views.handler500'

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('api/accounts/', include('Account.urls_api')),
                  path('api/home/', include('Home.urls_api')),
                  path('api/vehicle/', include('Vehicle.urls_api')),
                  path('api/company/', include('Company.urls_api')),
                  path('api/client', include('Client.urls_api')),
                  path('api/employee', include('Employee.urls_api')),
                  path('api/reservations/', include('Reservation.urls_api')),

                  path('', include('Company.urls')),
                  path('account/', include("Account.urls")),
                  path('client/', include("Client.urls")),
                  path('employee/', include("Employee.urls")),
                  path('vehicle/', include("Vehicle.urls")),
                  path('company/', include("Company.urls")),
                  path('setting/', include("setting.urls")),
                  path('accounting/', include("Accounting.urls")),



    # AGENTSTUDENT====================================================
                  path('agent/', include("Agent.urls")),
                  path('student/', include("Student.urls")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
