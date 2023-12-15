import os
from django.core.management.base import BaseCommand
from telegram.ext import (Updater, CommandHandler, MessageHandler, 
                          Filters, ConversationHandler, CallbackQueryHandler)
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests

import logging
from dotenv import load_dotenv

load_dotenv()


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

            return 'GET_GAME_NAME'

        def get_game_name(update, context):
            try:
                context.user_data['chat_id'] = update.effective_chat.id
                if update.message:
                    context.user_data['message_id'] = update.message.message_id
                    update.message.reply_text('Введите название игры:')
                    return 'CREATE_GAME'
                elif update.callback_query:
                    context.user_data['message_id'] = update.callback_query.message.message_id
                    context.bot.send_message(chat_id=update.effective_chat.id, text='Введите название игры:')
                    return 'CREATE_GAME'
                else:
                    raise ValueError('No message or callback query in update')
            except Exception as e:
                print(f"Error in get_game_name function: {e}")
                return ConversationHandler.END

        def create_game(update, context):
            try:
                game_name = update.message.text

                django_view_url = f'http://127.0.0.1:8000/create_game/'

                response = requests.post(django_view_url, json={'game_name': game_name})

                print(f"Sent POST request to Django for creating game: {game_name}")
                print(f"Response from Django: {response.text}")

                data_from_db = response.json()
                print(data_from_db)

                context.bot.send_message(chat_id=context.user_data['chat_id'],
                                         text=f'Игра "{game_name}" создана!')
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
                'CREATE_GAME': [MessageHandler(Filters.text & ~Filters.command, create_game)],
            },
            fallbacks=[],
        )

        dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()