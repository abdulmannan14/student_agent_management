from django.db import models
from django.contrib.auth.models import User
from Order import models as order_models


# Create your models here.
class TableModel(models.Model):
    AVAILABLE = "available"
    OCCUPIED = "occupied"
    table_status = [
        (AVAILABLE, AVAILABLE),
        (OCCUPIED, OCCUPIED)
    ]
    restaurant = models.ForeignKey('Restaurant.RestaurantModel', on_delete=models.CASCADE, null=True, blank=True)
    table_number = models.CharField(max_length=500, null=True, blank=True)
    table_status = models.CharField(max_length=500, choices=table_status, null=True, blank=True, default='available')
    # order_status = models.ForeignKey(order_models.OrderModel, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return "{table}".format(table=self.table_number)
