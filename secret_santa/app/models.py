from django.db import models


class Player(models.Model):
    tg_id = models.CharField(max_length=50, primary_key=True)
    login = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField(null=True)
    is_admin = models.BooleanField(default=False)
    wishes = models.TextField()

class Game(models.Model):
    name = models.CharField(max_length=255, blank=True, null=True)
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='owned_games', blank=True, null=True)
    players = models.ManyToManyField(Player, related_name='games', blank=True, null=True)
    is_limited = models.BooleanField(default=False, blank=True, null=True)
    budget = models.CharField(max_length=50, blank=True, null=True)
    draw_date = models.DateTimeField(blank=True, null=True)
    is_drawn = models.BooleanField(default=False, blank=True, null=True)
    send_date = models.DateTimeField(blank=True, null=True)


class DrawingResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE, blank=True, null=True)
    sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_gifts', blank=True, null=True)
    recipient = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='received_gifts', blank=True, null=True)