from django import forms

from . import models as accounting_models


class AssetForm(forms.ModelForm):
    class Meta:
        model = accounting_models.Asset
        fields = ['name', 'purchase_date', 'supported_date', 'amount', 'description']

        widgets = {

            "description": forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            "purchase_date": forms.DateInput(attrs={"type": "date", "style": "line-height: 20px !important"}),
            "supported_date": forms.DateInput(attrs={"type": "date", "style": "line-height: 20px !important"})

        }
