from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as menu_model
from django.core import validators


class MenuHeadForm(forms.ModelForm):
    class Meta:
        model = menu_model.MenuHead
        fields = ['name', ]
        # exclude = ('restaurant', 'date','time')


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = menu_model.MenuItem
        fields = ['name', 'price', 'menu_head', ]
        # exclude = ('restaurant', 'date','time')
