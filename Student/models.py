from django.db import models
from Courses import models as courses_models


# Create your models here.
class BaseModel(models.Model):
    objects = models.Manager()

    class Meta:
        abstract = True


completed_archive = 'COMPLETED ARCHIVE'
withdrawl_archive = 'WITHDRAWAL ARCHIVE'
refunded_archive = 'REFUNDED ARCHIVE'
archived_choices = [(completed_archive, completed_archive), (withdrawl_archive, withdrawl_archive),
                    (refunded_archive, refunded_archive)]
# Create your models here.


NO_COMMISSION = 'NO COMMISSION'
COMMISSION_ONLY = 'COMMISSION ONLY'
COMMISSION_PLUS_GST = 'COMMISSION + GST (10%)'
gst_choices = [
    (NO_COMMISSION, NO_COMMISSION),
    (COMMISSION_ONLY, COMMISSION_ONLY),
    (COMMISSION_PLUS_GST, COMMISSION_PLUS_GST)
]


class StudentCourse(models.Model):
    course = models.ForeignKey(courses_models.Course, on_delete=models.CASCADE, null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    commission = models.IntegerField(null=True, blank=True, default=30)
    commission_to_pay = models.IntegerField(null=True, blank=True, default=0)
    gst_status = models.CharField(max_length=30, choices=gst_choices, null=True, blank=True,
                                  default=COMMISSION_ONLY)
    material_fee = models.IntegerField(null=True, blank=True)
    tuition_fee = models.IntegerField(null=True, blank=True)
    application_fee = models.IntegerField(null=True, blank=True, default=250)
    quarterly_fee_amount = models.FloatField(null=True, blank=True)
    total_fee = models.FloatField(null=True, blank=True)
    oshc = models.IntegerField(null=True, blank=True)
    total_commission_amount = models.FloatField(null=True, blank=True)
    total_commission_paid = models.FloatField(null=True, blank=True)
    gst = models.IntegerField(null=True, blank=True, default=10)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.course.name


# Create your models here.
class StudentModel(BaseModel):
    agent_name = models.ForeignKey('Agent.AgentModel', on_delete=models.CASCADE, null=True, blank=True)
    acmi_number = models.CharField(max_length=500, null=True, blank=True)
    full_name = models.CharField(max_length=500, null=True, blank=True)
    courses = models.ManyToManyField(StudentCourse, null=True, blank=True)
    # start_date = models.DateField(null=True, blank=True)
    # end_date = models.DateField(null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    # material_fee = models.IntegerField(null=True, blank=True)
    # tuition_fee = models.IntegerField(null=True, blank=True)
    # application_fee = models.IntegerField(null=True, blank=True, default=250)
    application_fee_paid = models.BooleanField(null=True, blank=True, default=False)
    material_fee_paid = models.BooleanField(null=True, blank=True, default=False)
    oshc_fee_paid = models.BooleanField(null=True, blank=True, default=False)
    # discount = models.IntegerField(null=True, blank=True, default=0)
    # quarterly_fee_amount = models.FloatField(null=True, blank=True)
    # total_fee = models.FloatField(null=True, blank=True)
    # oshc = models.IntegerField(null=True, blank=True)
    outstanding_fee = models.FloatField(null=True, blank=True)
    total_required_fee = models.FloatField(null=True, blank=True)
    # total_commission_amount = models.FloatField(null=True, blank=True)
    total_commission_paid = models.FloatField(null=True, blank=True, default=0)
    paid_fee = models.FloatField(null=True, blank=True, default=0.0)
    previous_student_fee_history = models.CharField(max_length=500, null=True, blank=True)
    previous_commission_history = models.CharField(max_length=500, null=True, blank=True)
    # commission = models.IntegerField(null=True, blank=True, default=30)
    gst = models.IntegerField(null=True, blank=True, default=10)
    # gst_status = models.CharField(max_length=30, choices=gst_choices, null=True, blank=True, default=COMMISSION_ONLY)
    amount_already_inserted = models.BooleanField(default=False)
    amount_inserting_date = models.DateField(null=True, blank=True)
    last_paid_on = models.DateField(null=True, blank=True)

    warning_sent = models.BooleanField(default=False)
    refunded = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)
    archived_tag = models.CharField(max_length=50, null=True, blank=True, choices=archived_choices)

    refund_way = models.CharField(max_length=50, null=True, blank=True)
    refund_reason = models.TextField(null=True, blank=True)
    refund_amount = models.IntegerField(null=True, blank=True)
    commission_to_pay = models.FloatField(null=True, blank=True, default=0)
    quarters_paid = models.IntegerField(null=True, blank=True, default=0)

    # comment = models.TextField(null=True, blank=True)

    def __str__(self):
        return "{name}  ({acmi_number})".format(name=self.full_name, acmi_number=self.acmi_number)


tution_fee = 'Tuition Fee'
material_fee = 'Material Fee'
application_fee = 'Application Fee'
oshc_fee = 'OSHC Fee'
bonus = 'Bonus'
fee_type_choices = [(tution_fee, tution_fee), (material_fee, material_fee), (application_fee, application_fee),
                    (oshc_fee, oshc_fee), (bonus, bonus)]


# Create your models here.
class PayModelStudent(BaseModel):
    upfront_fee = 'UPFRONT FEE'
    adjustment = 'ADJUSTMENT'
    cash = "CASH"
    bank = "BANK TRANSFER"
    mode_of_payment_choices = [
        (cash, cash),
        (bank, bank),
        (upfront_fee, upfront_fee),
        (adjustment, adjustment)
    ]
    student = models.ForeignKey(StudentModel, on_delete=models.CASCADE, null=True, blank=True)
    student_course = models.ForeignKey(StudentCourse, on_delete=models.CASCADE, null=True, blank=True)
    fee_pay = models.FloatField(null=True, blank=True)
    paid_on = models.DateField(null=True, blank=True)
    fee_type = models.CharField(max_length=100, choices=fee_type_choices, null=True, blank=True)
    agent_commision_amount = models.FloatField(null=True, blank=True, default=0)
    comment = models.TextField(null=True, blank=True)
    mode_of_payment = models.CharField(max_length=100, choices=mode_of_payment_choices, null=True, blank=True)
    commission_percentage = models.IntegerField(null=True, blank=True)
    # outstanding_fee = models.IntegerField(null=True, blank=True)
    # total_required_fee = models.IntegerField(null=True, blank=True)
