from django import forms
from django.forms import ModelForm

from bots.models import BotUser
from games.models import Game
from .bot import generate_random_password


class CheckBoxInput(forms.CheckboxInput):
    input_type = "checkbox"


class BotGameCreateForm(ModelForm):
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

    def save(self, commit=True):
        game = super().save(commit=False)
        if not self.cleaned_data["using_special_stones"]:
            game.p1_has_thunder_stone = False
            game.p1_has_woden_stone = False
            game.p2_has_thunder_stone = False
            game.p2_has_woden_stone = False

        # Check for existing bot user
        bot_user, created = BotUser.objects.get_or_create(
            username="Aelfric",
            defaults={
                "password": generate_random_password(),
                "is_bot": True,
                "email": "Aelfric@example.com",
                "rating": 1000,
            }
        )

        game.player2 = bot_user

        if commit:
            game.save()
        return game
