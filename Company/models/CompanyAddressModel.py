from django.db import models


class CompanyAddressModel(models.Model):
    address = models.CharField(max_length=100, null=False, blank=False)
    city = models.CharField(max_length=50, null=False, blank=False)
    state = models.CharField(max_length=50, null=False, blank=False)
    zip_code = models.IntegerField(null=False, blank=False)


    def __str__(self):
        return self.address