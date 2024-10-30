from django import forms

from .models import Invitation


class InvitationCreateForm(forms.ModelForm):
    game_name = forms.CharField(max_length=100, required=True)

    class Meta:
        model = Invitation
        fields = ["game_name"]
