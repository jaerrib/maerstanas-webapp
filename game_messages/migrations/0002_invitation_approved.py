# Generated by Django 5.1.1 on 2024-10-29 23:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game_messages', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='invitation',
            name='approved',
            field=models.BooleanField(default=False),
        ),
    ]