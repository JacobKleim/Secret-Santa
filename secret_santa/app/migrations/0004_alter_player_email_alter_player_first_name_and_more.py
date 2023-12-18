# Generated by Django 4.2.8 on 2023-12-15 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_alter_player_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='player',
            name='first_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='player',
            name='game',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.game', verbose_name='Игра'),
        ),
        migrations.AlterField(
            model_name='player',
            name='last_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='player',
            name='phone',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='player',
            name='wishes',
            field=models.TextField(blank=True, null=True, verbose_name='Пожелания'),
        ),
    ]