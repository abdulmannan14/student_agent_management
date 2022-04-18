from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as restaurant_models
from django.core import validators


class ExpenseForm(forms.ModelForm):
    class Meta:
        model = restaurant_models.Expense
        fields = ['name', 'price']
        # exclude = ('restaurant', 'date','time')
