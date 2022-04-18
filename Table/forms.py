from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as table_model
from django.core import validators


class TableForm(forms.ModelForm):
    class Meta:
        model = table_model.TableModel
        fields = "__all__"
        exclude = ('restaurant', 'order_status',)


class OverviewTableForm(forms.ModelForm):
    class Meta:
        model = table_model.TableModel
        fields = "__all__"
        exclude = ('restaurant',)
