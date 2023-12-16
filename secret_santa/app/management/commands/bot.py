import os
import requests
import logging

from apscheduler.schedulers.background import BackgroundScheduler
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, ConversationHandler, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
from dotenv import load_dotenv
from apscheduler.triggers.cron import CronTrigger
from django.core.management.base import BaseCommand
from django_apscheduler.jobstores import DjangoJobStore


load_dotenv()


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        bot_token = os.environ['TG_TOKEN']
        logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.info('Bot started')

        def start(update, context):
            keyboard = [
                [InlineKeyboardButton("Создать игру", callback_data='Создать игру')],
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Организуй тайный обмен подарками, запусти праздничное настроение!',
                                      reply_markup=reply_markup)

            return 'GET_GAME_NAME'

        def get_game_name(update, context):
            context.chat_data['game_info'] = {}
            try:
                context.user_data['chat_id'] = update.effective_chat.id
                if update.message:
                    context.user_data['message_id'] = update.message.message_id
                    context.chat_data['game_info']['owner'] = update.message.from_user['id']
                    update.message.reply_text('Введите название игры:')
                    return 'GET_BUDGET'
                elif update.callback_query:
                    context.user_data['message_id'] = update.callback_query.message.message_id
                    context.chat_data['game_info']['owner'] = update.callback_query.from_user['id']
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите название игры:')
                    return 'GET_BUDGET'
                else:
                    raise ValueError('No message or callback query in update')
            except Exception as e:
                print(f"Error in get_game_name function: {e}")
                return 'ERROR'

        def get_budget(update, context):
            context.chat_data['game_info']['name'] = update.message.text
            keyboard = [
                ['Да', 'Нет']
            ]
            reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
            update.message.reply_text('Бюджет ограничен?', reply_markup=reply_markup)
            return 'CHOOSE_BUDGET'

        def choose_budget(update, context):
            if update.message.text == "Да":
                context.chat_data['game_info']['is_limited'] = True
                keyboard = [
                    ['до 500', '500-1000', '1000-2000']
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
                update.message.reply_text('Выберите бюджет:', reply_markup=reply_markup)
                return 'REGISTRATION_DATE'
            context.chat_data['game_info']['is_limited'] = False
            context.chat_data['game_info']['budget'] = ''
            update.message.reply_text('Введите дату завершения регистрации (в формате ММ/ДД/ГГГГ):')
            return 'CREATE_GAME'

        def get_registration_date(update, context):
            context.chat_data['game_info']['budget'] = update.message.text
            update.message.reply_text('Введите дату завершения регистрации (в формате ММ/ДД/ГГГГ):')
            return 'CREATE_GAME'

        def print_error_message(update, context):
            update.message.reply_text('Что-то пошло не так. Попробуйте ещё раз.')

        def create_game(update, context):
            context.chat_data['game_info']['draw_date'] = update.message.text
            game_info = context.chat_data['game_info']
            try:
                django_view_url = f'http://127.0.0.1:8000/create_game/'
                print(game_info)
                response = requests.post(django_view_url, json={
                    'owner': game_info['owner'],
                    'name': game_info['name'],
                    'is_limited': game_info['is_limited'],
                    'budget': game_info['budget'],
                    'draw_date': game_info['draw_date']
                }
                                         )

                print(f"Sent POST request to Django for creating game: {game_info}")
                print(f"Response from Django: {response.text}")

                data_from_db = response.json()
                print('----------')
                print(data_from_db)
                print('----------')

                update.message.reply_text(
                    f'Игра {data_from_db["name"]} создана! Ссылка на игру: https://t.me/sssssssssannnttaaaa_bot/start={data_from_db["id"]}')
                return ConversationHandler.END
            except Exception as e:
                print(f"Error in create_game function: {e}")
                return ConversationHandler.END

        updater = Updater(bot_token, use_context=True)
        dispatcher = updater.dispatcher

        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                'GET_GAME_NAME': [CallbackQueryHandler(get_game_name)],
                'GET_BUDGET': [MessageHandler(Filters.text & ~Filters.command, get_budget)],
                'CHOOSE_BUDGET': [MessageHandler(Filters.text & ~Filters.command, choose_budget)],
                'REGISTRATION_DATE': [MessageHandler(Filters.text & ~Filters.command, get_registration_date)],
                'CREATE_GAME': [MessageHandler(Filters.text & ~Filters.command, create_game)],
                'ERROR': [MessageHandler(Filters.text & ~Filters.command, print_error_message)],
            },
            fallbacks=[],
        )
        dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()

        def start_task():
            print("Дата наступила")

            scheduler = BackgroundScheduler()
            scheduler.add_jobstore(DjangoJobStore(), "default")
            draw_date = "2023-01-01 12:00:00"
            cron_trigger = CronTrigger(
                year=draw_date.year,
                month=draw_date.month,
                day=draw_date.day,
                hour=draw_date.hour,
                minute=draw_date.minute,
                second=draw_date.second,
            )

            scheduler.add_task(
                start_task,
                trigger=cron_trigger,
                id="my_task",
                max_instances=1,
                replace_existing=True,
                )

            logger.info("Added job 'my_task'.")

            try:
                logger.info("Starting scheduler...")
                scheduler.start()
            except KeyboardInterrupt:
                logger.info("Stopping scheduler...")
                scheduler.shutdown()
                logger.info("Scheduler shut down successfully!")
