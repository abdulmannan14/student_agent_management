from django.db import models

# Create your models here.
NO_COMMISSION = 'NO COMMISSION'
COMMISSION_ONLY = 'COMMISSION ONLY'
COMMISSION_PLUS_GST = 'COMMISSION + GST (10%)'
gst_choices = [
    (NO_COMMISSION, NO_COMMISSION),
    (COMMISSION_ONLY, COMMISSION_ONLY),
    (COMMISSION_PLUS_GST, COMMISSION_PLUS_GST)
]


class Course(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    description = models.CharField(max_length=500, null=True, blank=True)
    weeks = models.IntegerField(null=True, blank=True)
    months = models.IntegerField(null=True, blank=True)
    quarters = models.IntegerField(null=True, blank=True)
    # ===================


    def __str__(self):
        return self.name
