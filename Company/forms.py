from django import forms

from Company.models import CompanyProfileModel, CompanyAddressModel, CompanyPackage, PaymentInfo


class CompanyProfileForm(forms.ModelForm):
    class Meta:
        model = CompanyProfileModel
        fields = ["company_name", "phone", "secondary_phone"]
        widgets = {
            'company_name': forms.TextInput(attrs={'data_icon': 'fa fa-building', "required": ""}),
            'phone': forms.TextInput(attrs={'data_icon': 'fa fa-phone', "required": ""}),
            'secondary_phone': forms.TextInput(attrs={'data_icon': 'fa fa-phone'}),
        }


class CompanyAddressForm(forms.ModelForm):
    class Meta:
        model = CompanyAddressModel
        fields = "__all__"
        widgets = {
            'address': forms.TextInput(attrs={'data_icon': 'fa fa-address-card', "required": ""}),
            'city': forms.TextInput(attrs={'data_icon': 'fa fa-location-arrow', "required": ""}),
            'state': forms.TextInput(attrs={'data_icon': 'fa fa-globe', "required": ""}),
            'zip_code': forms.TextInput(attrs={'data_icon': 'fa fa-hashtag', "required": "", "type": "number"}),
        }


class CompanyPackageForm(forms.ModelForm):
    class Meta:
        model = CompanyPackage
        fields = ["package"]
        widgets = {
            "package": forms.Select(attrs={"data_icon": "fa fa-gift", "required": ""})
        }


class PaymentInfoForm(forms.ModelForm):
    class Meta:
        model = PaymentInfo
        exclude = ["address"]
        widgets = {
            'expiry_month': forms.Select(
                attrs={'data_icon': 'fa fa-calendar', "required": "", }),
            'expiry_year': forms.Select(
                attrs={'data_icon': 'fa fa-calendar', "required": "", }),
            'card_holder_name': forms.TextInput(
                attrs={'data_icon': 'fa fa-user', "required": ""}),
            'card_number': forms.TextInput(
                attrs={'data_icon': 'fa fa-hashtag', "required": ""}),
            'security_code': forms.TextInput(
                attrs={'data_icon': 'fa fa-lock', "required": "", }),
        }
