# import os
# from django.core.management.base import BaseCommand
# from telegram.ext import CommandHandler, CallbackContext, Updater
# from telegram import Update
import logging
from dotenv import load_dotenv
import json

load_dotenv()


# class Command(BaseCommand):
#     help = 'Starts the Telegram bot'

#     def handle(self, *args, **options):
#         logging.basicConfig(
#             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#             level=logging.INFO)

#         bot_token = os.environ['TELEGRAM_BOT_TOKEN']

#         def start(update: Update, context: CallbackContext):
#             update.message.reply_text('Hello! I am your bot.')

#         updater = Updater(bot_token, use_context=True)
#         dispatcher = updater.dispatcher

#         dispatcher.add_handler(CommandHandler('start', start))

#         updater.start_polling()

#         updater.idle()


# import os
# from django.core.management.base import BaseCommand
# from telegram.ext import (
#     CommandHandler,
#     CallbackContext,
#     Updater,
#     CallbackQueryHandler,
#     MessageHandler,
#     Filters,
#     ConversationHandler,
# )
# from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
# import logging
# from dotenv import load_dotenv

# load_dotenv()

# GAME_NAME, = range(1)

# class Command(BaseCommand):
#     help = 'Starts the Telegram bot'

#     def handle(self, *args, **options):
#         logging.basicConfig(
#             format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
#             level=logging.INFO)

#         bot_token = os.environ['TELEGRAM_BOT_TOKEN']

#         def start(update: Update, context: CallbackContext):
#             keyboard = [
#                 [InlineKeyboardButton("Создать игру", callback_data='Создать игру')],
#             ]
#             reply_markup = InlineKeyboardMarkup(keyboard)
#             update.message.reply_text('Организуй тайный обмен подарками, запусти праздничное настроение!',
#                                     reply_markup=reply_markup)

#             return GAME_NAME

#         def game_name(update: Update, context: CallbackContext):
#             context.user_data['game_name'] = update.message.text
#             context.bot.send_message(chat_id=update.effective_chat.id,
#                                     text=f'Игра "{context.user_data["game_name"]}" создана!')

#             return ConversationHandler.END

#         def button(update: Update, context: CallbackContext):
#             query = update.callback_query
#             query.answer()
#             query.edit_message_text(text="Создать игру")

#             context.bot.send_message(chat_id=update.effective_chat.id,
#                                     text='Введите название игры:')
#             return GAME_NAME

#         def create_game_command(update: Update, context: CallbackContext):
#             keyboard = [
#                 [InlineKeyboardButton("Создать игру", callback_data='Создать игру')],
#             ]
#             reply_markup = InlineKeyboardMarkup(keyboard)
#             update.message.reply_text('Организуй тайный обмен подарками, запусти праздничное настроение!',
#                                     reply_markup=reply_markup)

#             return GAME_NAME

#         def cancel_command(update: Update, context: CallbackContext):
#             update.message.reply_text('Операция отменена.')
#             return ConversationHandler.END

#         updater = Updater(bot_token, use_context=True)
#         dispatcher = updater.dispatcher

#         conv_handler = ConversationHandler(
#             entry_points=[CommandHandler("start", start)],
#             states={
#                 GAME_NAME: [MessageHandler(Filters.text & ~Filters.command, game_name)],
#             },
#             fallbacks=[],
#         )

#         dispatcher.add_handler(conv_handler)
#         dispatcher.add_handler(CallbackQueryHandler(button))
#         dispatcher.add_handler(CommandHandler("create_game", create_game_command))
#         dispatcher.add_handler(CommandHandler("cancel", cancel_command))

#         updater.start_polling()
#         updater.idle()        
import os
from django.core.management.base import BaseCommand
from telegram.ext import Updater, CommandHandler, CallbackContext, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from django.urls import reverse
from django.http import QueryDict
import requests

class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        bot_token = os.environ['TELEGRAM_BOT_TOKEN']
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

            return 'CREATE_GAME'

        def create_game(update, context):
            try:
        # Получаем переданное через кнопку название игры
                game_name = update.callback_query.data

                # Ваш существующий код
                django_view_url = f'http://127.0.0.1:8000/create_game/'  # Замените на ваш хост и порт

                # Используйте POST-запрос и передавайте данные в теле запроса
                response = requests.post(django_view_url, json={'game_name': game_name})

                # Добавим логи для проверки
                print(f"Sent POST request to Django for creating game: {game_name}")
                print(f"Response from Django: {response.text}")

                # Ваш код обработки ответа, если необходимо
                data_from_db = response.json()
                print(data_from_db)

                context.bot.send_message(chat_id=update.effective_chat.id,
                                        text=f'Игра "{game_name}" создана!')
                return ConversationHandler.END
            except Exception as e:
                print(f"Error in create_game function: {e}")
                return ConversationHandler.END

        updater = Updater(bot_token, use_context=True)
        dispatcher = updater.dispatcher

        # Добавляем обработчики состояний
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", start)],
            states={
                'CREATE_GAME': [CallbackQueryHandler(create_game)],
            },
            fallbacks=[],
        )

        dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()