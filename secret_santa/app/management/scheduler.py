from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from app.models import Game
from time import sleep


def check_games():
    games_to_draw = Game.objects.filter(draw_date__lte=timezone.now(), is_drawn=False)
    for game in games_to_draw:
        perform_lottery(game.id)


def perform_lottery(game_id):
    game = Game.objects.get(pk=game_id)
    if game:
        print(game.id)
        game.is_drawn = True
        game.save()


def start_task():
    scheduler = BackgroundScheduler()
    #scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(check_games, trigger='interval', seconds=60)
    try:
        scheduler.start()

    except KeyboardInterrupt:
        scheduler.shutdown()