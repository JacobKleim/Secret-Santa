import os
from django.core.management.base import BaseCommand
from telegram.ext import CommandHandler, CallbackContext, Updater
from telegram import Update
import logging
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO)

        bot_token = os.environ['TELEGRAM_BOT_TOKEN']

        def start(update: Update, context: CallbackContext):
            update.message.reply_text('Hello! I am your bot.')

        updater = Updater(bot_token, use_context=True)
        dispatcher = updater.dispatcher

        dispatcher.add_handler(CommandHandler('start', start))

        updater.start_polling()

        updater.idle()
