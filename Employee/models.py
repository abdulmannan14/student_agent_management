from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse

from Account.models import UserProfile
from Company import models as company_models


class EmployeeAddress(models.Model):
    address = models.CharField(max_length=100, null=False, blank=False)
    country = models.CharField(max_length=50, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    zip_code = models.CharField(max_length=20, null=False, blank=False)

    def __str__(self):
        return self.country


class EmployeeRole(models.Model):
    title = models.CharField(choices='', max_length=30, null=True, blank=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title


class EmployeeProfileModel(models.Model):
    DISPATCHER = "DISPATCHER"
    DRIVER = "DRIVER"
    MANAGER = "MANAGER"
    employee_roles = [
        (DRIVER, DRIVER),
        (DISPATCHER, DISPATCHER),
        (MANAGER, MANAGER),

    ]
    userprofile = models.OneToOneField(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    employee_role = models.CharField(max_length=40, null=False, blank=False,
                                     verbose_name="Position")
    # employee_role=models.ForeignKey(EmployeeRole,null=True,blank=True,on_delete=models.SET_NULL,)
    is_active = models.BooleanField(default=False, null=False, verbose_name="Work Status")
    primary_phone = models.CharField(max_length=30, null=False, blank=False,verbose_name='Phone Number')
    secondary_phone = models.CharField(max_length=30, null=True, blank=True)
    Client_Phone_Visible = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    company = models.ForeignKey(company_models.CompanyProfileModel, on_delete=models.CASCADE, null=True, blank=True)
    dark_mode = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        try:
            return "{} ({})({})".format(self.userprofile.user.get_full_name(), self.userprofile.user.username,
                                        self.employee_role)
        except:
            return "-"

    @property
    def full_name(self):
        return self.userprofile.user.get_full_name()

    @property
    def username(self):
        return self.userprofile.user.username

    @property
    def email(self):
        return self.userprofile.user.email
