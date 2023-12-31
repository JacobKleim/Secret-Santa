# Generated by Django 4.2.8 on 2023-12-15 15:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True)),
                ('is_limited', models.BooleanField(blank=True, default=False, null=True)),
                ('budget', models.CharField(blank=True, max_length=50, null=True)),
                ('draw_date', models.DateTimeField(blank=True, null=True)),
                ('send_date', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=50, null=True)),
                ('last_name', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('is_admin', models.BooleanField(blank=True, default=False, null=True)),
                ('wishes', models.TextField(blank=True, null=True)),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.game')),
            ],
        ),
        migrations.AddField(
            model_name='game',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owned_games', to='app.player'),
        ),
        migrations.AddField(
            model_name='game',
            name='players',
            field=models.ManyToManyField(blank=True, related_name='games', to='app.player'),
        ),
        migrations.CreateModel(
            name='DrawingResult',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('game', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.game')),
                ('recipient', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='received_gifts', to='app.player')),
                ('sender', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sent_gifts', to='app.player')),
            ],
        ),
    ]
