from django import forms
from django.forms import ModelForm

from bots.models import BotUser
from games.models import Game
from .bot import generate_random_password


class CheckBoxInput(forms.CheckboxInput):
    input_type = "checkbox"


class BotGameCreateForm(ModelForm):
    BOT_NAMES = [
        ("Oswin", "Oswin"),
        # ("Aelfric", "Aelfric"),
        # ("Aethelstan", "Aethelstan"),
    ]
    bot_name = forms.ChoiceField(choices=BOT_NAMES, required=True,
                                 label="Opponent")

    class Meta:
        model = Game
        fields = [
            "name",
            "using_special_stones",
            "using_standard_scoring",
            "bot_name",
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

        bot_name = self.cleaned_data["bot_name"]
        bot_user, created = BotUser.objects.get_or_create(
            username=bot_name,
            defaults={
                "password": generate_random_password(),
                "is_bot": True,
                "email": f"{bot_name}@example.com",
                "rating": 1000,
            },
        )

        game.player2 = bot_user

        if commit:
            game.save()
        return game
