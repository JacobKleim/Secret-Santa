from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from django.utils import timezone
from app.models import Game
from app.models import Player
from time import sleep


def check_games():
    games_to_draw = Game.objects.filter(draw_date__lte=timezone.now(), is_drawn=False)
    for game in games_to_draw:
        perform_lottery(game.id)


def perform_lottery(game_id):
    game = Game.objects.get(pk=game_id)
    if game:
        from random import shuffle
        players_tuple = game.players.values_list('tg_id')
        players = [int(tg_id) for tg_id, in players_tuple]
        shuffle(players)
        for i in range(-1, len(players)-1):
            print(f'{players[i]} дарит подарок {players[i+1]}')
            send_mailing()
        game.is_drawn = True
        game.save()

def send_mailing(update, context):
    player_tg = 
    # Iterate over the subscribers and send them a message
    for subscriber in subscribers:
        context.bot.send_message(chat_id=subscriber[0], text='Это тестовая рассылка')
        time.sleep(1)  # pause for 1 second before sending the next message
    # Respond to the user who sent the command
    update.message.reply_text('Рассылка отправлена!')

    # Close the connection and cursor
    c.close()
    conn.close()


def start_task():
    scheduler = BackgroundScheduler()
    #scheduler.add_jobstore(DjangoJobStore(), "default")
    scheduler.add_job(check_games, trigger='interval', seconds=60)
    try:
        scheduler.start()

    except KeyboardInterrupt:
        scheduler.shutdown()