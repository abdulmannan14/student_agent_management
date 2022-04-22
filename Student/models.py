from django.db import models


# Create your models here.

# Create your models here.
class StudentModel(models.Model):
    agent_name = models.ForeignKey('Agent.AgentModel', on_delete=models.CASCADE, null=True, blank=True)
    # agent_commission = models.IntegerField(null=True, blank=True, default=30)
    # agent_bonus = models.IntegerField(null=True, blank=True, default=0)
    acmi_number = models.CharField(max_length=500, null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    course = models.CharField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    non_refundable_fee = models.IntegerField(null=True, blank=True)
    material_fee = models.IntegerField(null=True, blank=True)
    tuition_fee = models.IntegerField(null=True, blank=True)
    application_fee = models.IntegerField(null=True, blank=True, default=250)
    discount = models.IntegerField(null=True, blank=True)
    total_fee = models.IntegerField(null=True, blank=True)
    outstanding_fee = models.IntegerField(null=True, blank=True)
    total_required_fee = models.IntegerField(null=True, blank=True)
    total_commission_amount = models.IntegerField(null=True, blank=True)
    paid_fee = models.IntegerField( null=True, blank=True)
    previous_student_fee_history = models.CharField(max_length=500, null=True, blank=True)
    previous_commission_history = models.CharField(max_length=500, null=True, blank=True)
    warning_sent = models.BooleanField(default=False)

    def __str__(self):
        return "{name}".format(name=self.full_name)


# Create your models here.
class PayModel(models.Model):
    agent = models.ForeignKey('Agent.AgentModel', on_delete=models.CASCADE, null=True, blank=True)
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE, null=True, blank=True)
    paid_fee = models.IntegerField(null=True, blank=True)
    paid_on = models.DateField(auto_now=True)
