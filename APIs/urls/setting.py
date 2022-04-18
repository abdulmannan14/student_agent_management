from django.urls import path
from APIs.views import settings as setting_views

urlpatterns = [
    path("get_service_types", setting_views.get_service_types),
    path("get_airprts", setting_views.get_airports),
    path("get_google_key/", setting_views.get_google_key),
]
