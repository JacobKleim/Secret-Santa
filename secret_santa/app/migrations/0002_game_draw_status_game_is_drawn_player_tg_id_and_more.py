# Generated by Django 4.2.8 on 2023-12-18 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='game',
            name='draw_status',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='game',
            name='is_drawn',
            field=models.BooleanField(blank=True, default=False, null=True),
        ),
        migrations.AddField(
            model_name='player',
            name='tg_id',
            field=models.CharField(blank=True, default=None, max_length=50, verbose_name='Telegram ID'),
        ),
        migrations.AlterField(
            model_name='game',
            name='name',
            field=models.CharField(default='Игра без названия', max_length=255, verbose_name='Название игры'),
        ),
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='first_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='player',
            name='game',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='app.game', verbose_name='Игра'),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_name',
            field=models.CharField(max_length=50, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=models.CharField(max_length=20, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='player',
            name='wishes',
            field=models.TextField(blank=True, default='Любой подарок', verbose_name='Пожелания'),
        ),
    ]