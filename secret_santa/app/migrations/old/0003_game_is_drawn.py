# Generated by Django 4.2.8 on 2023-12-16 17:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_game_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='is_drawn',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
    ]
