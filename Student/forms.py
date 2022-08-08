from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as student_models
from django.core import validators


class StudentForm(forms.ModelForm):
    start_date = forms.CharField(max_length=50, required=True,
                                 widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    course_quarters = forms.CharField(max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        super(StudentForm, self).__init__(*args, **kwargs)

        self.fields['acmi_number'].required = True
        self.fields['agent_name'].required = True
        self.fields['full_name'].required = True
        self.fields['course'].required = True
        self.fields['email'].required = True
        self.fields['tuition_fee'].required = True
        self.fields['material_fee'].required = True
        self.fields['application_fee'].required = True
        self.fields['commission'].required = True
        # self.fields['gst'].required = True
        self.fields['gst_status'].required = True

        # self.fields['total_required_fee'].widget.attrs['readonly'] = True
        self.fields['quarterly_fee_amount'].widget.attrs['readonly'] = True
        self.fields['total_fee'].widget.attrs['readonly'] = True
        self.fields['total_commission_amount'].widget.attrs['readonly'] = True
        self.fields['course_quarters'].widget.attrs['readonly'] = True
        self.fields['material_fee'].label = "Material Fee($)"
        self.fields['acmi_number'].label = "ACMi Number"
        self.fields['quarterly_fee_amount'].label = "Qaurterly Fee($)"
        self.fields['tuition_fee'].label = "Tuition Fee($)"
        # self.fields['total_required_fee'].label = "Total Required Fee($)"
        self.fields['total_fee'].label = "Total Fee($)"
        self.fields['application_fee'].label = "Application Fee($)"
        self.fields['agent_name'].label = " Agent Company"
        self.fields['discount'].label = "Discount($)"
        self.fields['total_commission_amount'].label = "Total Commission Amount($)"
        self.fields['course_quarters'].label = "Course Quarters"

        self.fields['oshc'].label = "OSHC Fee ($)"

    class Meta:
        model = student_models.StudentModel
        fields = ['agent_name', 'acmi_number', 'full_name', 'phone', 'email', 'course', 'course_quarters', 'discount',
                  'start_date', 'end_date', 'commission', 'gst_status', 'material_fee', 'tuition_fee',
                  'application_fee', 'quarterly_fee_amount', 'total_fee', 'oshc', 'total_commission_amount','comment']
        # exclude = ['paid_fee', 'previous_student_fee_history', 'warning_sent', 'previous_commission_history',
        #            'outstanding_fee', 'last_paid_on', 'total_commission_paid', 'amount_already_inserted',
        #            'amount_inserting_date', 'commission_to_pay', 'application_fee_paid', 'material_fee_paid',
        #            'refunded', 'refund_reason', 'refund_amount', 'quarters_paid', 'oshc_fee_paid']


class StudentFormEdit(forms.ModelForm):
    start_date = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    end_date = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    course_quarters = forms.CharField(max_length=20, required=True)

    def __init__(self, *args, **kwargs):
        super(StudentFormEdit, self).__init__(*args, **kwargs)
        self.fields['acmi_number'].required = True
        self.fields['agent_name'].required = True
        self.fields['full_name'].required = True
        self.fields['course'].required = True
        self.fields['email'].required = True
        self.fields['tuition_fee'].required = True
        self.fields['material_fee'].required = True
        self.fields['application_fee'].required = True
        self.fields['commission'].required = True
        # self.fields['gst'].required = True
        self.fields['gst_status'].required = True

        # self.fields['total_required_fee'].widget.attrs['readonly'] = True
        self.fields['quarterly_fee_amount'].widget.attrs['readonly'] = True
        self.fields['total_fee'].widget.attrs['readonly'] = True
        self.fields['total_commission_amount'].widget.attrs['readonly'] = True
        self.fields['course_quarters'].widget.attrs['readonly'] = True
        self.fields['paid_fee'].widget.attrs['readonly'] = True
        self.fields['material_fee'].label = "Material Fee($)"
        self.fields['acmi_number'].label = "ACMi Number"
        self.fields['quarterly_fee_amount'].label = "Qaurterly Fee($)"
        self.fields['tuition_fee'].label = "Tuition Fee($)"
        # self.fields['total_required_fee'].label = "Total Required Fee($)"
        self.fields['total_fee'].label = "Total Fee($)"
        self.fields['application_fee'].label = "Application Fee($)"
        self.fields['agent_name'].label = " Agent Company"
        self.fields['discount'].label = "Discount($)"
        self.fields['total_commission_amount'].label = "Total Commission Amount($)"
        self.fields['course_quarters'].label = "Course Quarters"

        self.fields['oshc'].label = "OSHC Fee ($)"

    class Meta:
        model = student_models.StudentModel
        fields = ['agent_name', 'acmi_number', 'full_name', 'phone', 'email', 'course', 'course_quarters', 'discount',
                  'start_date', 'end_date', 'commission', 'gst_status', 'material_fee', 'tuition_fee',
                  'application_fee', 'quarterly_fee_amount', 'total_fee', 'paid_fee','oshc', 'total_commission_amount','total_required_fee','comment']
        # exclude = ['total_commission_paid', 'paid_fee', 'previous_student_fee_history', 'previous_commission_history',
        #            'amount_inserting_date', 'amount_already_inserted', 'last_paid_on', 'application_fee_paid',
        #            'material_fee_paid', 'refunded', 'refund_reason', 'refund_amount', 'quarters_paid', 'oshc_fee_paid',
        #            'commission_to_pay']


class AddFeeForm(forms.ModelForm):
    paid_on = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(AddFeeForm, self).__init__(*args, **kwargs)
        self.fields['fee_pay'].label = "Fee Amount"
        self.fields['paid_on'].label = "Date"
        self.fields['is_oshc_fee'].label = "OSHC Fee"
        self.fields['is_material_fee'].label = "Material Fee"
        self.fields['is_application_fee'].label = "Application Fee"
        self.fields['student'].required = True
        self.fields['fee_pay'].required = True
        # self.fields['total_required_fee'].label = "Total Required Fee($)"
        # self.fields['outstanding_fee'].label = "Outstanding Fee($)"

    class Meta:
        model = student_models.PayModelStudent
        fields = ['student', 'fee_pay', 'mode_of_payment', 'paid_on', 'is_material_fee', 'is_application_fee',
                  'is_oshc_fee',
                  'comment']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': '5', 'cols': '3'}),
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
        fields = ['student', 'fee_pay', 'mode_of_payment', 'paid_on', 'is_material_fee', 'is_application_fee',
                  'comment']


class StudentFormAddFee(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(StudentFormAddFee, self).__init__(*args, **kwargs)
        self.fields['total_fee'].widget.attrs['readonly'] = True
        self.fields['paid_fee'].widget.attrs['readonly'] = True
        self.fields['total_required_fee'].widget.attrs['readonly'] = True
        self.fields['outstanding_fee'].widget.attrs['readonly'] = True
        self.fields['total_required_fee'].label = "Total Required Fee($)"
        self.fields['outstanding_fee'].label = "Outstanding Fee($)"

    class Meta:
        model = student_models.StudentModel
        fields = ['total_required_fee', 'outstanding_fee', 'total_fee', 'paid_fee']
