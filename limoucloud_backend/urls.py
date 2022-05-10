from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# from django.conf.urls import (
#     handler400, handler403, handler404, handler500
# )
#
# handler404 = 'Home.views.handler404'
# handler500 = 'Home.views.handler500'

urlpatterns = [
                  path('admin/', admin.site.urls),
                  # AGENTSTUDENT====================================================
                  path('', include('Student.urls')),
                  path('agent/', include("Agent.urls")),
                  path('student/', include("Student.urls")),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
