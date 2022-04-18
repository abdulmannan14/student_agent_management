from Account.utils import _get_user
from Employee.models import EmployeeProfileModel
from django.contrib.auth.models import User


def get_driver(user: User = None, username=None, email=None, userprofile=None):
    """
    get driver or employee model object if any of above param is given
    """
    if user:
        pass
    elif userprofile:
        user = userprofile.user
    elif username:
        user = _get_user(username=username)
    elif email:
        user = _get_user(email=email.lower())
    return _get_employee_profile_model_from_user(user)


def _get_employee_profile_model_from_user(user):
    
    if user and user.userprofile:
        return user.userprofile.employeeprofilemodel
    return None
