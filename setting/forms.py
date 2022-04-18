from django import forms
from . import models as setting_models


class VehicleTypeForm(forms.ModelForm):
    class Meta:
        model = setting_models.VehicleType
        fields = "__all__"
        exclude = ['company', 'image']


class ServicePriceFormForMinimumHour(forms.ModelForm):
    class Meta:
        model = setting_models.ServicePrice
        fields = ('minimum_hours',)


class ServiceTypeForm(forms.ModelForm):
    round_trip = forms.BooleanField(required=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].required = True

    class Meta:
        model = setting_models.ServiceType
        fields = "__all__"
        exclude = ['company', ]


class ServicePriceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(ServicePriceForm, self).__init__(*args, **kwargs)
        self.fields['sales_tax'].required = True
        self.fields['sales_tax_percentage'].readonly = True
        self.fields['sales_tax_percentage'].widget.attrs['readonly'] = True

    class Meta:
        model = setting_models.ServicePrice
        fields = "__all__"
        exclude = ['flat_rate', 'distance_rate', 'hourly_rate', 'minimum_hours', 'zone_to_zone_rate']


class ServiceAreaForm(forms.ModelForm):
    class Meta:
        model = setting_models.ServiceArea
        fields = ("name",)


class ZoneAreaForm(forms.ModelForm):
    class Meta:
        model = setting_models.Zone
        fields = ("name",)


class AirportsForm(forms.ModelForm):
    class Meta:
        model = setting_models.CompanyAirport
        fields = ("airport",)


class VehicleTypePriceForDistance(forms.ModelForm):
    class Meta:
        model = setting_models.Distance
        fields = "__all__"


class VehicleTypePriceForZoneToZone(forms.ModelForm):
    class Meta:
        model = setting_models.ZoneToZone
        fields = "__all__"


class VehicleTypePriceForFlatRate(forms.ModelForm):
    class Meta:
        model = setting_models.AirportToServiceArea
        fields = ('airport',)


class VehicleTypePriceForHourlyRate(forms.ModelForm):
    class Meta:
        model = setting_models.Hour
        fields = "__all__"


class FlatRateForm(forms.ModelForm):
    class Meta:
        model = setting_models.AirportToServiceArea
        fields = "__all__"


class PaymentsForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(PaymentsForm, self).__init__(*args, **kwargs)
        self.fields['publish_key'].label = "Publishable Key"

    # publish_key = forms.CharField
    class Meta:
        model = setting_models.StripePayment
        fields = ("publish_key", "secret_key",)


class FeedbackForm(forms.ModelForm):
    # message=forms.TextInput()
    class Meta:
        model = setting_models.Feedback
        fields = "__all__"
        widgets = {
            'message': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
        }


class SalesTaxForm(forms.ModelForm):
    name = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'id': 'tax_name'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = True
        self.fields['name'].label = "Tax name"
        self.fields['abbreviation'].required = True

    class Meta:
        model = setting_models.SalesTax
        fields = ['name', 'abbreviation', 'tax_number', 'show_on_invoice', 'recoverable', 'compound', 'description']


#
# class SalesTaxFormForPricing(forms.ModelForm):
#     class Meta:
#         model = setting_models.SalesTax
#         fields = ['name']


class TaxRateFormForAdd(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(TaxRateFormForAdd, self).__init__(*args, **kwargs)
        self.fields['rate'].required = True
        self.fields['rate'].label = "Tax rate(%)"

    class Meta:
        model = setting_models.TaxRate
        fields = ['rate', ]


class TaxRateFormForEdit(forms.ModelForm):
    effective_date = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super(TaxRateFormForEdit, self).__init__(*args, **kwargs)
        self.fields['rate'].label = "New Tax rate(%)"

    class Meta:
        model = setting_models.TaxRate
        fields = ['rate', 'effective_date']
