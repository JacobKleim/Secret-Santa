# Generated by Django 4.2.8 on 2023-12-17 21:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_game_registration_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='registration_status',
            new_name='draw_status',
        ),
    ]
