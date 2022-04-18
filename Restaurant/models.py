from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class RestaurantModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=False, null=False)
    name = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    last_paid_date = models.DateField(null=True, blank=True)
    active_status = models.BooleanField(default=False)
    sales_tax = models.IntegerField(null=True, blank=True)
    created_at = models.DateField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return "{name}".format(name=self.name)


class Expense(models.Model):
    restaurant = models.ForeignKey(RestaurantModel, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    time = models.TimeField(auto_now_add=True, null=True, blank=True)
