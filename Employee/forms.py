from django import forms
from .models import *
from Account.models import *


class EmployeeProfileForm(forms.ModelForm):
    class Meta:
        model = EmployeeProfileModel
        fields = (
            'primary_phone',
            'secondary_phone',
            # 'Client_Phone_Visible',
            # 'is_active'
        )

class EmployeeProfileFormForPosition(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(EmployeeProfileFormForPosition, self).__init__(*args, **kwargs)
        self.fields['title'].label = "Positions"
    class Meta:
        model = EmployeeRole
        fields = (
            'title',
        )

class EmployeeAddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address',]


class UserForm(forms.ModelForm):
    # password=forms.PasswordInput()
    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = "__all__"
