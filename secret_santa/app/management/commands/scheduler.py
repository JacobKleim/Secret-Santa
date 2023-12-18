import logging
import requests
import pytz
import os

from apscheduler.schedulers.background import BackgroundScheduler
from django.core.management.base import BaseCommand
from django.utils import timezone
from app.models import DrawingResult, Game, Player
from dotenv import load_dotenv
from random import shuffle

load_dotenv()
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)


def send_message(sender, recipient, success):
    logger = logging.getLogger(__name__)
    logger.info('sending message from {} to {}'.format(sender.tg_id, recipient.tg_id))
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    send_date = recipient.game.send_date.astimezone(pytz.timezone('Europe/Moscow')).strftime('%d-%m-%Y %H:%M')
    if success:
        text = f'''Розыгрыш проведен!\n
Вы дарите подарок 🎁 пользователю {recipient.first_name} {recipient.last_name}!
Вот пожелания пользователя - {recipient.wishes}.
Дата отправки подарка до {send_date}
'''

    else:
        text = f'Розыгрыш не был проведен, слишком мало участников! Подарите подарок себе 🎁'
    data = {
        'chat_id': sender.tg_id,
        'text': text
    }
    response = requests.post(url, data=data)
    return response.json()


def perform_lottery():
    games_to_draw = Game.objects.filter(draw_date__lte=timezone.now(), draw_status=False)
    for game in games_to_draw:
        players = list(Player.objects.filter(game=game))
        if len(players) < 2:
            send_message(players[0], players[0], False)
        else:
            shuffle(players)
            print(players)
            for i in range(len(players)):
                sender = players[i]
                recipient = players[(i + 1) % len(players)]
                DrawingResult.objects.create(
                    game=game, sender=sender, recipient=recipient)
                logger = logging.getLogger(__name__)
                response = send_message(sender, recipient, True)
                logger.info(response)
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
