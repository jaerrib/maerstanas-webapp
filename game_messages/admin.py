from django.contrib import admin

from .models import Invitation, SystemNotice


class CustomInvitationAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "game",
        "sender",
        "receiver",
    ]

class CustomSystemNoticeAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "message_text",
    ]

admin.site.register(Invitation, CustomInvitationAdmin)
admin.site.register(SystemNotice, CustomSystemNoticeAdmin)
