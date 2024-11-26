from django import forms
from django.forms import ModelForm

from .models import Invitation


class CheckBoxInput(forms.CheckboxInput):
    input_type = "checkbox"


class InvitationCreateForm(ModelForm):
    game_name = forms.CharField(max_length=100, required=True)
    using_special_stones = forms.BooleanField(required=False, initial=True)
    using_standard_scoring = forms.BooleanField(required=False, initial=True)

    class Meta:
        model = Invitation
        fields = ["game_name", "using_special_stones", "using_standard_scoring"]
        widgets = {
            "using_special_stones": CheckBoxInput(),
            "using_standard_scoring": CheckBoxInput(),
        }
