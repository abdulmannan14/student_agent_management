from django.contrib import admin
from limoucloud_backend.admin_utils import set_app_models_to_admin

# Register your models here.

from .DoubleEntry.models import *

# admin.site.register(ChartOfAccount)
# set_app_models_to_admin("DoubleEntry")
