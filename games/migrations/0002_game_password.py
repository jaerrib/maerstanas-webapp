# Generated by Django 5.1.1 on 2024-10-16 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('games', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='password',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
