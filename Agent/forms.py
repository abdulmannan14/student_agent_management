from django import forms
from django.core.exceptions import ValidationError
import re
from . import models as agent_models
from django.core import validators


class AgentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        self.fields['bonus'].label = "bonus($)"
    class Meta:
        model = agent_models.AgentModel
        fields = "__all__"
        # exclude = ('restaurant', 'date','time')
