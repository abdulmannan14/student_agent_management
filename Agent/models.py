from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


# Create your models here.
class AgentModel(BaseModel):
    INCLUSIVE = 'INCLUSIVE'
    EXCLUSIVE = 'EXCLUSIVE'
    gst_choices = [
        (INCLUSIVE, INCLUSIVE),
        (EXCLUSIVE, EXCLUSIVE)
    ]
    company = models.CharField(max_length=500, null=True, blank=True)
    name = models.CharField(max_length=500, null=True, blank=True)
    country = models.CharField(max_length=500, null=True, blank=True)
    bonus = models.IntegerField(null=True, blank=True, default=0)
    commission = models.IntegerField(null=True, blank=True, default=30)
    gst = models.IntegerField(null=True, blank=True, default=10)
    gst_status = models.CharField(max_length=30, choices=gst_choices, null=True, blank=True, default=EXCLUSIVE)
    # commission_get= models.IntegerField(null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)

    def __str__(self):
        return "{name}".format(name=self.company)


# Create your models here.
class CommissionModelAgent(BaseModel):
    student = models.ForeignKey('Student.StudentModel', on_delete=models.CASCADE, null=True, blank=True)
    agent_name = models.CharField(max_length=100, null=True)
    agent_commission_percentage = models.CharField(max_length=100, null=True)
    agent_commission_amount = models.CharField(max_length=100, null=True)
    total_commission_paid = models.CharField(max_length=100, null=True)
    student_paid_fee = models.CharField(max_length=100, null=True)
    current_commission_amount = models.CharField(max_length=100, null=True)
    paid_on = models.DateField(null=True, blank=True)
    # commission_left = models.IntegerField(null=True, blank=True)
