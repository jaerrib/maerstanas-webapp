import uuid

from django.contrib.auth import get_user_model
from django.db import models

from games.models import Game


class Invitation(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(
        get_user_model(), related_name="sent_invitations", on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        get_user_model(), related_name="received_invitations", on_delete=models.CASCADE
    )
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    approved = models.BooleanField(default=False)


class SystemNotice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name="system_messages")
    message_text = models.CharField(max_length=255)

    def __str__(self):
        return self.message_text
