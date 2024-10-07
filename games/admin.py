from django.contrib import admin

from .models import Game, GameBoard, MovesLeftList, PlayedMovesList


class GameBoardAdmin(admin.ModelAdmin):
    list_display = ["id"]


class PlayedMovesListAdmin(admin.ModelAdmin):
    list_display = ["id"]


class MovesLeftListAdmin(admin.ModelAdmin):
    list_display = ["id"]


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
admin.site.register(GameBoard, GameBoardAdmin)
admin.site.register(MovesLeftList, MovesLeftListAdmin)
admin.site.register(PlayedMovesList, PlayedMovesListAdmin)
