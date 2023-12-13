from django.db import models

class Player(models.Model):
    tg_id = models.CharField(max_length=50, primary_key=True)
    login = models.CharField(max_length=50)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False)
    wishes = models.TextField()
    game_id = models.ForeignKey('Game', on_delete=models.CASCADE)

class Game(models.Model):
    owner = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='owned_games')
    players = models.ManyToManyField(Player, related_name='games')
    is_limited = models.BooleanField(default=False)
    budget = models.CharField(max_length=50)
    draw_date = models.DateTimeField()
    send_date = models.DateTimeField()

class DrawingResult(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    sender = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='sent_gifts')
    recipient = models.ForeignKey(Player, on_delete=models.CASCADE, related_name='received_gifts')