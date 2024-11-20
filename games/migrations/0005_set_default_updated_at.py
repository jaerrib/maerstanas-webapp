# Generated by Django 5.1.1 on 2024-11-18 17:48

import datetime

from django.db import migrations


def set_default_updated_at(apps, schema_editor):
    Game = apps.get_model('games', 'Game')
    for obj in Game.objects.all():
        obj.updated_at = datetime.datetime.now()
        obj.save()

class Migration(migrations.Migration):

    dependencies = [
        ('games', '0004_game_updated_at'),
    ]

    operations = [
        migrations.RunPython(set_default_updated_at),
    ]
