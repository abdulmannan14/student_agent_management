from django.db import models


# Create your models here.
class AgentModel(models.Model):
    name = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    bonus = models.IntegerField(null=True,blank=True)
    commission = models.IntegerField(null=True,blank=True,default=30)
    phone = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return "{name}".format(name=self.name)
