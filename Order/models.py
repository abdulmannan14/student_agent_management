from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class OrderModel(models.Model):
    ORDERED = "Ordered"
    IN_PROGRESS = "In Progress"
    SERVED = "Served"
    COMPLETED = "Completed"
    order_status = [
        (ORDERED, ORDERED),
        (IN_PROGRESS, IN_PROGRESS),
        (SERVED, SERVED),
        (COMPLETED, COMPLETED),
    ]
    restaurant = models.ForeignKey('Restaurant.RestaurantModel', on_delete=models.CASCADE, null=True, blank=True)
    table = models.ForeignKey('Table.TableModel', on_delete=models.CASCADE, null=True, blank=True)
    order_items = models.CharField(max_length=5000, null=True, blank=True)
    status = models.CharField(max_length=500, choices=order_status, null=True, blank=True)
    bill = models.CharField(max_length=500, null=True, blank=True)
    bill_paid = models.BooleanField(null=True, blank=True, default=False)
    date = models.DateField(auto_now_add=True, null=True, blank=True)
    time = models.TimeField(auto_now_add=True, null=True, blank=True)
    feedback = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{status},{bill}".format(status=self.status, bill=self.bill)
