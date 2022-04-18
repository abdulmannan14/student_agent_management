from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as vehicle_models
from django.core import validators


class VehicleForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['vehicle_type'].required = True
        self.fields['all_vehicle_name'].label = "Vehicles"

    tabs_expiration_date = forms.CharField(max_length=50, required=True, widget=forms.TextInput(attrs={'type': 'date'}))
    inspection_expiration_date = forms.CharField(max_length=50, required=True,
                                                 widget=forms.TextInput(attrs={'type': 'date'}))

    class Meta:
        model = vehicle_models.Vehicle
        # fields="__all__"
        fields = ['all_vehicle_name', 'vehicle_type', 'vin', 'year', 'make', 'model_name', 'vehicle_number',
                  'plate_number', 'color', 'milage', 'insurance_company', 'driver', 'driver', 'tabs_expiration_date',
                  'inspection_expiration_date']
        # exclude=('company','is_on_ride','license','last_ride_started_milage','last_ride_ending_milage','image')


class VehicleChecklistForm(forms.ModelForm):
    class Meta:
        model = vehicle_models.Checklist
        fields = "__all__"
        exclude = ('fluids', 'lights', 'brake_and_tyres', 'misc',)


class ChecklistFluidForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChecklistFluidForm, self).__init__(*args, **kwargs)
        self.fields['fluid_comments'].label = "Comments"

    class Meta:
        model = vehicle_models.Fluid
        fields = "__all__"


class ChecklistBrakesForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChecklistBrakesForm, self).__init__(*args, **kwargs)
        self.fields['break_comments'].label = "Comments"

    class Meta:
        model = vehicle_models.BrakeTyre
        fields = "__all__"


class ChecklistLightForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChecklistLightForm, self).__init__(*args, **kwargs)
        self.fields['light_comments'].label = "Comments"

    # comments = forms.CharField("Lights Comments", max_length=500)
    class Meta:
        model = vehicle_models.Light
        fields = "__all__"


class ChecklistMiscForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ChecklistMiscForm, self).__init__(*args, **kwargs)
        self.fields['misc_comments'].label = "Comments"

    # comments = forms.CharField("Miscellaneous Comments", max_length=500)
    class Meta:
        model = vehicle_models.Misc
        fields = "__all__"
