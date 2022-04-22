from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as student_models
from django.core import validators


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['acmi_number'].label = "ACMi Number"
        # self.fields['agent_commission'].label = "Agent Commission(%)"
        # self.fields['agent_commission'].widget.attrs['readonly'] = True
        self.fields['total_required_fee'].widget.attrs['readonly'] = True
        self.fields['total_fee'].widget.attrs['readonly'] = True
        self.fields['non_refundable_fee'].label = "Non Refundable Fee($)"
        self.fields['material_fee'].label = "Material Fee($)"
        self.fields['tuition_fee'].label = "Tuition Fee($)"
        self.fields['total_required_fee'].label = "Total Required Fee($)"
        # self.fields['paid_fee'].label = "Paid Fee($)"
        self.fields['total_fee'].label = "Total Fee($)"
        self.fields['application_fee'].label = "Application Fee($)"
        # self.fields['commission'].label = "Commission(%)"
        # self.fields['agent_bonus'].label = "Agent Bonus($)"
        self.fields['discount'].label = "Discount($)"
        self.fields['total_commission_amount'].label = "Total Commission Amount($)"

    class Meta:
        model = student_models.StudentModel
        fields = "__all__"
        exclude = ['paid_fee', 'previous_student_fee_history', 'warning_sent', 'previous_commission_history',
                   'outstanding_fee']


class StudentFormEdit(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)
        self.fields['acmi_number'].label = "ACMi Number"
        # self.fields['agent_commission'].label = "Agent Commission(%)"
        # self.fields['agent_commission'].widget.attrs['readonly'] = True
        self.fields['total_required_fee'].widget.attrs['readonly'] = True
        self.fields['non_refundable_fee'].label = "Non Refundable Fee($)"
        self.fields['material_fee'].label = "Material Fee($)"
        self.fields['tuition_fee'].label = "Tuition Fee($)"
        self.fields['total_required_fee'].label = "Total Required Fee($)"
        # self.fields['paid_fee'].label = "Paid Fee($)"
        self.fields['outstanding_fee'].label = "Outstanding Fee($)"
        self.fields['application_fee'].label = "Application Fee($)"
        # self.fields['commission'].label = "Commission(%)"
        # self.fields['agent_bonus'].label = "Agent Bonus($)"
        self.fields['discount'].label = "Discount($)"
        self.fields['total_commission_amount'].label = "Total Commission Amount($)"

    class Meta:
        model = student_models.StudentModel
        fields = "__all__"
