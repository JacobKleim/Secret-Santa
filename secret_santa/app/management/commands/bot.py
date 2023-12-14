import os
from django.core.management.base import BaseCommand
from telegram.ext import CommandHandler, CallbackContext, Updater, CallbackQueryHandler, ConversationHandler
from telegram.ext import MessageHandler, Filters
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

        create_game, get_game_name = range(2)

        def start(update: Update, context: CallbackContext):
            keyboard = [
                [InlineKeyboardButton("Создать игру", callback_data='Создать игру')],

            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            update.message.reply_text('Организуй тайный обмен подарками, запусти праздничное настроение!',
                                      reply_markup=reply_markup)
            return create_game

        def button(update, _):
            query = update.callback_query
            query.answer()
            query.edit_message_text(text="Создать игру")
            if query.data == 'create_game':
                query.edit_message_text(text="Игра успешно создана! Теперь давайте уточним детали.")

            return get_game_name

        def get_game_name(update: Update, context: CallbackContext):
            game_name = update.message.text
            update.message.reply_text(f"Название игры: {game_name}")

            return ConversationHandler.END

        conv_handler = ConversationHandler(
            entry_points=[MessageHandler(Filters.text & ~Filters.command, start)],
            states={
                create_game: [CallbackQueryHandler(button)],
                get_game_name: [MessageHandler(Filters.text & ~Filters.command, get_game_name)],
            },
            fallbacks=[],
        )

        updater = Updater(bot_token, use_context=True)
        dispatcher = updater.dispatcher
        # dispatcher.add_handler(CommandHandler("start", start))
        # dispatcher.add_handler(CallbackQueryHandler(button))
        dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.stop()

