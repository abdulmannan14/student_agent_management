from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as student_models
from django.core import validators


class CourseForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(CourseForm, self).__init__(*args, **kwargs)
        # self.fields['acmi_number'].label = "ACMi Number"
        # self.fields['acmi_number'].required = True
        # self.fields['agent_name'].required = True
        # self.fields['full_name'].required = True
        # self.fields['course'].required = True
        # self.fields['email'].required = True
        # self.fields['tuition_fee'].required = True
        # self.fields['material_fee'].required = True
        # self.fields['application_fee'].required = True
        # self.fields['total_required_fee'].widget.attrs['readonly'] = True
        # self.fields['quarterly_fee_amount'].widget.attrs['readonly'] = True
        # self.fields['total_fee'].widget.attrs['readonly'] = True
        # self.fields['material_fee'].label = "Material Fee($)"
        # self.fields['quarterly_fee_amount'].label = "Qaurterly Fee($)"
        # self.fields['tuition_fee'].label = "Tuition Fee($)"
        # self.fields['total_required_fee'].label = "Total Required Fee($)"
        # self.fields['total_fee'].label = "Total Fee($)"
        # self.fields['application_fee'].label = "Application Fee($)"
        # self.fields['agent_name'].label = " Agent Company"
        # self.fields['discount'].label = "Discount($)"
        # self.fields['total_commission_amount'].label = "Total Commission Amount($)"
        self.fields['quarters'].widget.attrs['readonly'] = True
        self.fields['months'].widget.attrs['readonly'] = True

    class Meta:
        model = student_models.Course
        fields = "__all__"
