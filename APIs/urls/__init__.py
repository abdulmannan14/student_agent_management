from django.urls import path, include

from .driver import *
from .client import *

urlpatterns = [
    path("driver/", include("APIs.urls.driver")),
    path("client/", include("APIs.urls.client")),
    path("account/", include("APIs.urls.account")),
    path("vehicle/", include("APIs.urls.vehicle")),
    path("setting/", include("APIs.urls.setting")),
]
