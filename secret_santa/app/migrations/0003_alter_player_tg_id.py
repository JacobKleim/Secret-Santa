# Generated by Django 4.2.8 on 2023-12-19 12:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_game_draw_status_game_is_drawn_player_tg_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='tg_id',
            field=models.CharField(default=None, max_length=50, verbose_name='Telegram ID'),
        ),
    ]
