# Generated by Django 5.1.1 on 2024-11-18 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0003_game_is_archived_for_p1_game_is_archived_for_p2'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
