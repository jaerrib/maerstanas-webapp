from django.contrib import admin

from .models import Invitation, SystemNotice

admin.site.register(Invitation)
admin.site.register(SystemNotice)
