from django.db import models


# Create your models here.


class Course(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    weeks = models.IntegerField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    quarters = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name
