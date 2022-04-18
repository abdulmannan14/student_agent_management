from django import forms
from django.contrib.auth.models import User

from Account.models import UserProfile, Address
from . import models as client_models


class PersonalClientProfileForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PersonalClientProfileForm, self).__init__(*args, **kwargs)
        self.fields['primary_phone'].required = True

    class Meta:
        model = client_models.PersonalClientProfileModel
        fields = "__all__"
        exclude = ['userprofile', 'business_client', 'client_payment_info', 'company', 'is_corporate_client',
                   'merchant_account', 'is_client_active']


class ClientPaymentInfoForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ClientPaymentInfoForm, self).__init__(*args, **kwargs)
        self.fields['payment_method'].required = True
    # card_name = forms.CharField(max_length=50,required=False)
    # card_number = forms.CharField(max_length=50,required=False)
    # card_expiration_date = forms.CharField(max_length=50,required=False,widget=forms.TextInput(attrs={'type':'date'}))
    # cvv=forms.IntegerField()
    class Meta:
        model = client_models.ClientPaymentInfoModel
        fields = ['payment_method']
        # fields = "__all__"


class BusinessClientProfileForm(forms.ModelForm):
    business_name = forms.CharField(max_length=50, required=True)
    business_phone = forms.CharField(max_length=50, required=True)

    class Meta:
        model = client_models.BusinessClientProfileModel
        fields = "__all__"


class EditBusinessClientProfileForm(forms.ModelForm):
    class Meta:
        model = client_models.BusinessClientProfileModel
        fields = "__all__"


class EditClientPaymentInfoForm(forms.ModelForm):
    # cvv=forms.IntegerField(max_length=3,min_length=3)
    class Meta:
        model = client_models.ClientPaymentInfoModel
        fields = "__all__"
        widgets = {
            "card_expiration_date": forms.DateInput(attrs={'type': "date"}),
        }


class EditPersonalClientProfileForm(forms.ModelForm):
    class Meta:
        model = client_models.PersonalClientProfileModel
        fields = "__all__"
        exclude = ['userprofile', 'business_client', 'client_payment_info', 'company', 'is_corporate_client',
                   'merchant_account']


class UserForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True
        self.fields['username'].required = True

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email',)


class AddressForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['address'].required = True

    class Meta:
        model = Address
        fields = ('address',)


class ClientOverviewProfileForm(forms.ModelForm):
    class Meta:
        model = client_models.PersonalClientProfileModel
        fields = "__all__"
        exclude = ['userprofile', 'business_client', 'client_payment_info', 'merchant_account', 'company',
                   'is_client_active', 'is_corporate_client']
