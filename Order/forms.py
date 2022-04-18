from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as order_model
from django.core import validators


class OrderForm(forms.ModelForm):
    class Meta:
        model = order_model.OrderModel
        fields = "__all__"
        exclude = ('restaurant', 'date','time','feedback')

#
# class OvervieworderForm(forms.ModelForm):
#     class Meta:
#         model = order_model.OrderModel
#         fields = "__all__"
#         exclude = ('restaurant',)

# class OrderFeedbackForm()