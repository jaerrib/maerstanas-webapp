from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import BotUser


class BotUserAdmin(UserAdmin):
    model = BotUser
    list_display = [
        "email",
        "username",
        "is_superuser",
        "games_won",
        "games_lost",
        "games_tied",
        "games_played",
        "win_percentage",
        "games_abandoned",
        "rating",
        "is_bot",
    ]


admin.site.register(BotUser, BotUserAdmin)
