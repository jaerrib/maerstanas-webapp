from django import forms
from django.forms import ModelForm

from .models import Game


class CheckBoxInput(forms.CheckboxInput):
    input_type = "checkbox"


class GameCreateForm(ModelForm):
    class Meta:
        model = Game
        fields = [
            "name",
            "using_special_stones",
            "using_standard_scoring",
        ]
        widgets = {
            "using_special_stones": CheckBoxInput(),
            "using_standard_scoring": CheckBoxInput(),
        }


class GameUpdateForm(ModelForm):
    class Meta:
        model = Game
        fields = [
            "name",
            "using_special_stones",
            "using_standard_scoring",
        ]
        widgets = {
            "using_special_stones": CheckBoxInput(),
            "using_standard_scoring": CheckBoxInput(),
        }
