from django.db import models


# Create your models here.
class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


# Create your models here.
class StudentModel(BaseModel):
    agent_name = models.ForeignKey('Agent.AgentModel', on_delete=models.CASCADE, null=True, blank=True)
    acmi_number = models.CharField(max_length=500, null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    course = models.CharField(max_length=500, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    # non_refundable_fee = models.IntegerField(null=True, blank=True)
    material_fee = models.IntegerField(null=True, blank=True)
    tuition_fee = models.IntegerField(null=True, blank=True)
    application_fee = models.IntegerField(null=True, blank=True, default=250)
    application_fee_paid = models.BooleanField(null=True, blank=True, default=False)
    material_fee_paid = models.BooleanField(null=True, blank=True, default=False)
    discount = models.IntegerField(null=True, blank=True, default=0)
    quarterly_fee_amount = models.FloatField(null=True, blank=True)
    total_fee = models.FloatField(null=True, blank=True)
    outstanding_fee = models.FloatField(null=True, blank=True)
    total_required_fee = models.FloatField(null=True, blank=True)
    total_commission_amount = models.FloatField(null=True, blank=True)
    total_commission_paid = models.FloatField(null=True, blank=True, default=0)
    paid_fee = models.FloatField(null=True, blank=True, default=0.0)
    previous_student_fee_history = models.CharField(max_length=500, null=True, blank=True)
    previous_commission_history = models.CharField(max_length=500, null=True, blank=True)
    amount_already_inserted = models.BooleanField(default=False)
    amount_inserting_date = models.DateField(null=True, blank=True)
    last_paid_on = models.DateField(null=True, blank=True)
    warning_sent = models.BooleanField(default=False)
    commission_to_pay = models.FloatField(null=True, blank=True, default=0)

    def __str__(self):
        return "{name}".format(name=self.full_name)


# Create your models here.
class PayModelStudent(BaseModel):
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE, null=True, blank=True)
    fee_pay = models.FloatField(null=True, blank=True)
    paid_on = models.DateField(null=True, blank=True)
    is_material_fee = models.BooleanField(blank=True, default=False)
    is_application_fee = models.BooleanField(blank=True, default=False)
    is_tuition_and_material_fee = models.BooleanField(blank=True, default=False)
    agent_commision_amount = models.FloatField(null=True, blank=True, default=0)
    # outstanding_fee = models.IntegerField(null=True, blank=True)
    # total_required_fee = models.IntegerField(null=True, blank=True)
