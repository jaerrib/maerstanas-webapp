from django.contrib import admin

from .models import Game


class GameAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "player1",
        "player2",
        "score_p1",
        "score_p2",
        "using_special_stones",
        "using_standard_scoring",
    ]


admin.site.register(Game, GameAdmin)
