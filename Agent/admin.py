from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(AgentModel)
admin.site.register(CommissionModelAgent)
