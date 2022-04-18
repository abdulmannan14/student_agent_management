from functools import wraps

from rest_framework.response import Response

from Account import models as account_models
from django.contrib.auth.models import User
from Company import models as company_models
from Client import models as client_models
from Employee import models as employee_models
from .utils import failure_response


def _is_company_or_manager(user: User):
    try:
        userprofile = user.userprofile
        if userprofile.role == account_models.UserProfile.COMPANY and userprofile.companyprofilemodel:
            return True
        elif userprofile.role == account_models.UserProfile.MANAGER:
            if userprofile.employeeprofilemodel:
                pass
            return True
        else:
            return False
    except:
        return False


def _is_manager_or_dispatcher(user: User):
    try:
        userprofile = user.userprofile
        if userprofile.role == account_models.UserProfile.DISPATCHER and userprofile.employeeprofilemodel:
            return True
        elif userprofile.role == account_models.UserProfile.MANAGER:
            return True
        else:
            return False
    except:
        return False


def _is_manager_or_dispatcher_or_company(user: User):
    try:
        userprofile = user.userprofile
        if userprofile.role == account_models.UserProfile.DISPATCHER and userprofile.employeeprofilemodel:
            return True
        elif userprofile.role == account_models.UserProfile.MANAGER:
            return True
        elif userprofile.role == account_models.UserProfile.COMPANY and userprofile.companyprofilemodel:
            return True
        else:
            return False
    except:
        return False


def _is_company(user: User):
    try:
        userprofile = user.userprofile
        if userprofile.role == account_models.UserProfile.COMPANY and userprofile.companyprofilemodel:
            return True
        else:
            return False
    except:
        return False


def _is_client(user: User):
    try:
        userprofile = user.userprofile
        if userprofile.role == account_models.UserProfile.CLIENT and userprofile.personalclientprofilemodel:
            return True
        else:
            return False
    except:
        return False


def _is_employee_dispatcher(user: User):
    try:
        userprofile = user.userprofile
        if userprofile.role == account_models.UserProfile.DISPATCHER and userprofile.employeeprofilemodel:
            return True
        else:
            return False
    except:
        return False


def _is_employee_manager(user: User):
    try:
        userprofile = user.userprofile
        if userprofile.role == account_models.UserProfile.MANAGER:
            return True
        else:
            return False
    except:
        return False


def _is_employee_driver(user: User):
    try:
        userprofile = user.userprofile
        if userprofile.role == account_models.UserProfile.DRIVER and userprofile.employeeprofilemodel:
            return True
        else:
            return False
    except:
        return False


def _is_superuser(user: User):
    try:
        userprofile = user.is_superuser
        if userprofile:
            return True
        else:
            return False
    except:
        return False


def user_passes_test(passed_function,
                     default_response=failure_response(msg="You are not authorized to perform this action!")):
    """
    Decorator for views that checks that the user passes the given test,
    responding failure view if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if passed_function(request.user):
                return view_func(request, *args, **kwargs)
            return Response(default_response)

        return _wrapped_view

    return decorator
