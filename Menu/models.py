from django.db import models


# Create your models here.
class MenuHead(models.Model):
    restaurant = models.ForeignKey('Restaurant.RestaurantModel', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)

    def save(self, *args, **kwargs):
        for field_name in ['name', ]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(MenuHead, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    restaurant = models.ForeignKey('Restaurant.RestaurantModel', on_delete=models.CASCADE, null=True, blank=True)
    menu_head = models.ForeignKey('Menu.MenuHead', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        for field_name in ['name', ]:
            val = getattr(self, field_name, False)
            if val:
                setattr(self, field_name, val.capitalize())
        super(MenuItem, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
