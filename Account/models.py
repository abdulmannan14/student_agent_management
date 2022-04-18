from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Address(models.Model):
    address = models.CharField(max_length=500, blank=True, null=True)
    apartment = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    zip_code = models.IntegerField(null=True, blank=True)
    latitude=models.FloatField(null=True,blank=True)
    longitude=models.FloatField(null=True,blank=True)

    def __str__(self):
        return self.address


class Configuration(models.Model):
    dark_mode = models.BooleanField(default=False, null=True, blank=True)
    location = models.BooleanField(default=False, null=True, blank=True)
    new_trips_notifications = models.BooleanField(default=False, null=True, blank=True)
    notification = models.BooleanField(default=False, null=True, blank=True)
    storage = models.BooleanField(default=False, null=True, blank=True)


class UserProfile(models.Model):
    DISPATCHER = "DISPATCHER"
    DRIVER = "DRIVER"
    MANAGER = "MANAGER"
    COMPANY = 'COMPANY'
    CLIENT = 'CLIENT'

    employee_roles = [
        (DISPATCHER, DISPATCHER),
        (MANAGER, MANAGER),
        (DRIVER, DRIVER),
        (COMPANY, COMPANY),
        (CLIENT, CLIENT),

    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    image = models.ImageField(null=True, default="users/user-profile-small.png", upload_to="users/")
    phone = models.CharField(max_length=50, null=True, blank=True)
    email_verified = models.BooleanField(null=False, blank=False, default=False)
    verification_code = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=False)
    updated_at = models.DateTimeField(auto_now=True, null=False)

    def __str__(self):
        try:
            return "{}".format(self.user.username)
            # return "{} ({})".format(self.userprofile.user.get_full_name(), self.userprofile.user.username)
        except:
            return "None"

    @property
    def name(self):
        return self.user.get_full_name()

    @property
    def email(self):
        return self.user.email
