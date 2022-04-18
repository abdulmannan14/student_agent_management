from django import forms

from . import models as double_entry_models
from django.forms import formset_factory


class JournalEntryForm(forms.ModelForm):
    class Meta:
        model = double_entry_models.JournalEntry
        fields = ['journal_no', 'dated', 'description']
        # exclude = ["company", "transaction"]

        widgets = {
            "journal_no": forms.TextInput(attrs={"data_icon": "fas fa-file"}),
            "description": forms.Textarea(attrs={'rows': 3, 'cols': 50}),
            "dated": forms.TextInput(attrs={"type": "date", "data_icon": "fas fa-calendar"})
        }


class JournalItemForm(forms.ModelForm):
    class Meta:
        model = double_entry_models.JournalItem
        fields = ['account', 'debit', 'credit', 'description']
        widgets = {
            "account": forms.Select(attrs={"class": "form-control select2"}),
            "debit": forms.TextInput(attrs={"class": "form-control debit"}),
            "credit": forms.TextInput(attrs={"class": "form-control credit"}),
        }
        # exclude = ["company", "transaction"]

# JournalItemFormset = formset_factory(JournalItemForm)
