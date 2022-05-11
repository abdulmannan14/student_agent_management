from django import forms

from . import models as agent_models


class AgentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        self.fields['bonus'].label = "bonus($)"
        self.fields['name'].required = True
        self.fields['email'].required = True
        self.fields['country'].required = True
        self.fields['phone'].required = True
        self.fields['commission'].required = True
        self.fields['company'].required = True

    class Meta:
        model = agent_models.AgentModel
        fields = "__all__"
        # exclude = ('restaurant', 'date','time')


class AgentCommissionForm(forms.ModelForm):
    # agent_name = forms.CharField(max_length=100, required=False)
    # agent_commission_percentage = forms.CharField(max_length=100, required=False)
    # agent_commission_amount = forms.CharField(max_length=100, required=False)
    # total_commission_paid = forms.CharField(max_length=100, required=False)
    # student_paid_fee = forms.CharField(max_length=100, required=False)
    # current_commission_amount = forms.CharField(max_length=100, required=False)
    paid_on = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(AgentCommissionForm, self).__init__(*args, **kwargs)

        self.fields['agent_name'].label = "Agent Name"
        self.fields['agent_commission_amount'].widget.attrs['readonly'] = True
        self.fields['total_commission_paid'].widget.attrs['readonly'] = True
        self.fields['student_paid_fee'].widget.attrs['readonly'] = True
        self.fields['agent_commission_percentage'].widget.attrs['readonly'] = True

    class Meta:
        model = agent_models.CommissionModelAgent
        fields = "__all__"