from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as student_models
from django.core import validators
from Courses import models as course_models


class StudentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields['acmi_number'].required = True
        self.fields['agent_name'].required = True
        self.fields['full_name'].required = True
        self.fields['email'].required = True
        self.fields['acmi_number'].label = "ACMi Number"
        self.fields['agent_name'].label = " Agent Company"

    class Meta:
        model = student_models.StudentModel
        fields = ['agent_name', 'acmi_number', 'full_name', 'email', 'phone']


#
# class StudentForm(forms.ModelForm):
#     start_date = forms.CharField(max_length=50, required=True,
#                                  widget=forms.DateInput(attrs={'type': 'date'}))
#     end_date = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))
#     course_quarters = forms.CharField(max_length=20, required=True)
#
#     def __init__(self, *args, **kwargs):
#         super(StudentForm, self).__init__(*args, **kwargs)
#
#         self.fields['acmi_number'].required = True
#         self.fields['agent_name'].required = True
#         self.fields['full_name'].required = True
#         self.fields['course'].required = True
#         self.fields['email'].required = True
#         self.fields['tuition_fee'].required = True
#         self.fields['material_fee'].required = True
#         self.fields['application_fee'].required = True
#         self.fields['commission'].required = True
#         # self.fields['gst'].required = True
#         self.fields['gst_status'].required = True
#
#         # self.fields['total_required_fee'].widget.attrs['readonly'] = True
#         self.fields['quarterly_fee_amount'].widget.attrs['readonly'] = True
#         self.fields['total_fee'].widget.attrs['readonly'] = True
#         self.fields['total_commission_amount'].widget.attrs['readonly'] = True
#         self.fields['course_quarters'].widget.attrs['readonly'] = True
#         self.fields['material_fee'].label = "Material Fee($)"
#         self.fields['acmi_number'].label = "ACMi Number"
#         self.fields['quarterly_fee_amount'].label = "Qaurterly Fee($)"
#         self.fields['tuition_fee'].label = "Tuition Fee($)"
#         # self.fields['total_required_fee'].label = "Total Required Fee($)"
#         self.fields['total_fee'].label = "Total Fee($)"
#         self.fields['application_fee'].label = "Application Fee($)"
#         self.fields['agent_name'].label = " Agent Company"
#         self.fields['discount'].label = "Discount($)"
#         self.fields['total_commission_amount'].label = "Total Commission Amount($)"
#         self.fields['course_quarters'].label = "Course Quarters"
#
#         self.fields['oshc'].label = "OSHC Fee ($)"
#
#     class Meta:
#         model = student_models.StudentModel
#         fields = ['agent_name', 'acmi_number', 'full_name', 'phone', 'email', 'course', 'course_quarters', 'discount',
#                   'start_date', 'end_date', 'commission', 'gst_status', 'material_fee', 'tuition_fee',
#                   'application_fee', 'quarterly_fee_amount', 'total_fee', 'oshc', 'total_commission_amount','comment']
#

class StudentFormEdit(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(StudentFormEdit, self).__init__(*args, **kwargs)
        self.fields['acmi_number'].required = True
        self.fields['agent_name'].required = True
        self.fields['full_name'].required = True
        self.fields['email'].required = True
        self.fields['acmi_number'].label = "ACMi Number"
        self.fields['agent_name'].label = " Agent Company"

    class Meta:
        model = student_models.StudentModel
        fields = ['agent_name', 'acmi_number', 'full_name', 'phone', 'email']


class AddFeeForm(forms.ModelForm):
    paid_on = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    course = forms.ModelChoiceField(queryset=course_models.Course.objects.all(), required=True)

    # fee_type = forms.Select(choices=['Tuition Fee', 'Material Fee', 'Application Fee', 'OSHC Fee', 'Bonus'],
    # attrs = {'class': 'select2'})

    def __init__(self, *args, **kwargs):
        super(AddFeeForm, self).__init__(*args, **kwargs)
        self.fields['fee_pay'].label = "Fee Amount"
        self.fields['paid_on'].label = "Date"
        # self.fields['is_oshc_fee'].label = "OSHC Fee"
        # self.fields['is_material_fee'].label = "Material Fee"
        # self.fields['is_application_fee'].label = "Application Fee"
        # self.fields['student'].required = True
        self.fields['fee_pay'].required = True
        self.fields['fee_type'].required = True
        # self.fields['total_required_fee'].label = "Total Required Fee($)"
        # self.fields['outstanding_fee'].label = "Outstanding Fee($)"

    class Meta:
        model = student_models.PayModelStudent
        fields = ['course', 'fee_type', 'fee_pay', 'mode_of_payment', 'paid_on',
                  'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': '5', 'cols': '3'}),
            #     make fee type field is a select field

        }


class EditFeeForm(forms.ModelForm):
    paid_on = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(EditFeeForm, self).__init__(*args, **kwargs)
        self.fields['fee_pay'].label = "Fee Amount"
        self.fields['paid_on'].label = "Date"
        self.fields['student'].required = True
        self.fields['fee_pay'].required = True
        # self.fields['total_required_fee'].label = "Total Required Fee($)"
        # self.fields['outstanding_fee'].label = "Outstanding Fee($)"

    class Meta:
        model = student_models.PayModelStudent
        fields = ['student', 'fee_pay', 'mode_of_payment', 'paid_on', 'fee_type',
                  'comment']


class StudentFormAddFee(forms.ModelForm):
    total_fee = forms.FloatField(required=True)

    def __init__(self, *args, **kwargs):
        super(StudentFormAddFee, self).__init__(*args, **kwargs)
        self.fields['total_fee'].widget.attrs['readonly'] = True
        self.fields['paid_fee'].widget.attrs['readonly'] = True
        # self.fields['total_required_fee'].widget.attrs['readonly'] = True
        # self.fields['outstanding_fee'].widget.attrs['readonly'] = True
        # self.fields['total_required_fee'].label = "Total Required Fee($)"
        # self.fields['outstanding_fee'].label = "Outstanding Fee($)"
        self.fields['total_fee'].label = "Total Fee($)"
        self.fields['paid_fee'].label = "Paid Fee($)"

    class Meta:
        model = student_models.StudentModel
        # fields = ['total_required_fee', 'outstanding_fee', 'total_fee', 'paid_fee']
        fields = ['total_fee', 'paid_fee']
        # fields = "__all__"


class AddCourseForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddCourseForm, self).__init__(*args, **kwargs)
        self.fields['course'].required = True
        # self.fields['course_code'].required = True
        self.fields['material_fee'].label = "Material Fee($)"
        self.fields['tuition_fee'].label = "Tuition Fee($)"
        self.fields['application_fee'].label = "Application Fee($)"
        self.fields['quarterly_fee_amount'].label = "Qaurterly Fee($)"
        self.fields['total_fee'].label = "Total Fee($)"
        self.fields['total_commission_amount'].label = "Total Commission($)"
        self.fields['discount'].label = "Discount($)"

        # self.fields['course_code'].label = "Course Code"
        self.fields['total_fee'].widget.attrs['readonly'] = True
        self.fields['total_commission_amount'].widget.attrs['readonly'] = True
        self.fields['quarterly_fee_amount'].widget.attrs['readonly'] = True

    class Meta:
        model = student_models.StudentCourse
        fields = ['course', 'discount', 'start_date', 'end_date', 'commission', 'gst_status', 'material_fee',
                  'tuition_fee', 'application_fee', 'oshc', 'quarterly_fee_amount', 'total_fee',
                  'total_commission_amount', 'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': '5', 'cols': '3'}),
            # make the name field select2
            # 'course': forms.Select(attrs={'class': 'select2'}),
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }
