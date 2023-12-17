from django.db import models


class Player(models.Model):
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    phone = models.CharField('Телефон', max_length=20)
    email = models.EmailField()
    is_admin = models.BooleanField(default=False, blank=True, null=True)
    wishes = models.TextField('Пожелания', blank=True, null=True)
    game = models.ForeignKey(
        'Game',
        on_delete=models.CASCADE,
        verbose_name='Игра')

    def __str__(self):
        return (f'{self.first_name} {self.last_name}, '
                f'email: {self.email}, игра: {self.game}')


class Game(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name='Название игры')

    owner = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='owned_games',
        blank=True,
        null=True)

    players = models.ManyToManyField(Player, related_name='games', blank=True)
    is_limited = models.BooleanField(default=False, blank=True, null=True)
    budget = models.CharField(max_length=50, blank=True, null=True)
    draw_date = models.DateTimeField(blank=True, null=True)
    send_date = models.DateTimeField(blank=True, null=True)
    draw_status = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.name


class DrawingResult(models.Model):
    game = models.ForeignKey(
        Game, on_delete=models.CASCADE,
        blank=True, null=True)

    sender = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='sent_gifts',
        blank=True,
        null=True)

    recipient = models.ForeignKey(
        Player,
        on_delete=models.CASCADE,
        related_name='received_gifts',
        blank=True,
        null=True)
