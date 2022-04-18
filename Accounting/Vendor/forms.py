from django import forms
from . import models as vendor_models


class VendorForm(forms.ModelForm):
    class Meta:
        model = vendor_models.Vendor
        fields = ["name", "contact", "email", "vendor_type", "billing_name", "country", "state", "city",
                  "billing_phone",
                  "zip", "address"]

    widgets = {
        'name': forms.TextInput(attrs={'data_icon': 'fa fa-user', "required": ""})
    }
