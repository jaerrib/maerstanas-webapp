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
            "password",
        ]
        widgets = {
            "using_special_stones": CheckBoxInput(),
            "using_standard_scoring": CheckBoxInput(),
        }

    def save(self, commit=True):
        game = super().save(commit=False)
        game.set_password(self.cleaned_data["password"])
        if commit:
            game.save()
        return game


class GameUpdateForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Game
        fields = [
            "name",
            "using_special_stones",
            "using_standard_scoring",
            "password",
        ]
        widgets = {
            "using_special_stones": CheckBoxInput(),
            "using_standard_scoring": CheckBoxInput(),
        }

    def save(self, commit=True):
        game = super().save(commit=False)
        game.set_password(self.cleaned_data["password"])
        if commit:
            game.save()
        return game


class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)
