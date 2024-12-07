from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm

CustomUser = get_user_model()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
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


admin.site.register(CustomUser, CustomUserAdmin)
