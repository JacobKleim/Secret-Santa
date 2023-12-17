import logging

import pytz
from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from django.utils import timezone

from app.models import DrawingResult, Game, Player


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)


def perform_lottery():
    games_to_draw = Game.objects.filter(draw_date__lte=timezone.now())
    for game in games_to_draw:
        if game.draw_status is False:
            players = list(Player.objects.filter(game=game))
            for i in range(len(players)):
                sender = players[i]
                recipient = players[(i + 1) % len(players)]
                DrawingResult.objects.create(
                    game=game, sender=sender, recipient=recipient)

            game.draw_status = True
            game.save()


def start_task():
    scheduler = BackgroundScheduler(timezone=pytz.timezone('Europe/Moscow'))
    scheduler.add_job(perform_lottery, trigger='interval', seconds=60)
    try:
        scheduler.start()

    except KeyboardInterrupt:
        scheduler.shutdown()


class Command(BaseCommand):
    help = 'Run the scheduler'

    def handle(self, *args, **options):
        perform_lottery()
