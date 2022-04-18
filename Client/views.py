from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
# from . import models as client_models
from Account.utils import random_digits
from .tables import *
from .forms import *
from Company import models as company_models
from limoucloud_backend import decorators as backend_decorators


# Create your views here.


# @login_required
@user_passes_test(backend_decorators._is_company_or_manager)
def index(request):
    return render(request, "dashboard/client/index.html")


