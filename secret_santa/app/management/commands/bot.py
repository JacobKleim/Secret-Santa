import os
from django.core.management.base import BaseCommand
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import logging
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        bot_token = os.environ['TG_TOKEN']

        def start(update: Update, context: CallbackContext):
            keyboard = [
                [InlineKeyboardButton("Создать игру", callback_data='Создать игру')],

            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Организуй тайный обмен подарками, запусти праздничное настроение!',
                                      reply_markup=reply_markup)

        def button(update, _):
            query = update.callback_query
            query.answer()
            query.edit_message_text(text="Создать игру")

        updater = Updater(bot_token, use_context=True)
        dispatcher = updater.dispatcher
        dispatcher.add_handler(CommandHandler("start", start))
        dispatcher.add_handler(CallbackQueryHandler(button))


        updater.start_polling()
        updater.idle()

