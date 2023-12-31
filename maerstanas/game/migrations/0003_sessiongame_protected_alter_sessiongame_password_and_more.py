# Generated by Django 4.2.3 on 2023-10-02 23:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_alter_sessiongame_player_one_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='sessiongame',
            name='protected',
            field=models.BooleanField(default=False, verbose_name=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='sessiongame',
            name='password',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='sessiongame',
            name='status',
            field=models.CharField(max_length=10),
        ),
    ]
