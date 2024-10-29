from django import forms

from .models import Invitation, Game


class InvitationCreateForm(forms.ModelForm):
    game_name = forms.CharField()

    class Meta:
        model = Invitation
        fields = ["sender"]

    def save(self, commit=True):
        invitation = super().save(commit=False)
        game_name = self.cleaned_data.get("game_name")

        if game_name:
            game = Game.objects.create(
                name=game_name, player1=invitation.sender, player2=invitation.receiver
            )
            invitation.game = game

        if commit:
            invitation.save()
        return invitation
