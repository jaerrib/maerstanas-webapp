# Generated by Django 4.2.3 on 2023-08-22 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='ties',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
