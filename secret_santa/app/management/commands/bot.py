import logging
import os
import requests

from app.models import Player
from django.core.management.base import BaseCommand
from dotenv import load_dotenv
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup,
                      ReplyKeyboardMarkup)
from telegram.ext import (CallbackQueryHandler, CommandHandler,
                          ConversationHandler, Filters, MessageHandler,
                          Updater)


load_dotenv()


class Command(BaseCommand):
    help = 'Starts the Telegram bot'

    def handle(self, *args, **options):
        bot_token = os.environ['TELEGRAM_BOT_TOKEN']
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.DEBUG)
        logger = logging.getLogger(__name__)
        logger.info('Bot started')

        def start(update, context):
            admin_players = Player.objects.filter(is_admin=True).values_list('tg_id')
            WHITELIST = [int(tg_id) for tg_id, in admin_players]
            game_id = update.message.text.split(' ')[1] if len(update.message.text.split(' ')) > 1 else None
            if game_id:
                context.user_data['user_tg_id'] = update.message.from_user['id']
                context.user_data['game_id'] = game_id
                return register_user(update, context, game_id)
            else:
                if update.message.from_user['id'] in WHITELIST:
                    keyboard = [
                        [InlineKeyboardButton("Создать игру", callback_data='Создать игру')],
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    update.message.reply_text('Организуй тайный обмен подарками, запусти праздничное настроение!',
                                            reply_markup=reply_markup)
                    return 'GET_GAME_NAME'
                else:
                    update.message.reply_text('Вы не организатор! Перейдите по ссылке и зарегистрируйтесь как игрок!')

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
            reply_markup = ReplyKeyboardMarkup(keyboard,
                                               one_time_keyboard=True)
            update.message.reply_text('Бюджет ограничен?',
                                      reply_markup=reply_markup)
            return 'CHOOSE_BUDGET'

        def choose_budget(update, context):
            if update.message.text == "Да":
                context.chat_data['game_info']['is_limited'] = True
                keyboard = [
                    ['до 500', '500-1000', '1000-2000']
                ]
                reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
                update.message.reply_text('Выберите бюджет:', 
                                          reply_markup=reply_markup)
                return 'REGISTRATION_DATE'
            context.chat_data['game_info']['is_limited'] = False
            context.chat_data['game_info']['budget'] = ''
            update.message.reply_text('Введите дату завершения регистрации (в формате ММ/ДД/ГГГГ HH:MM):')
            return 'CREATE_GAME'

        def get_registration_date(update, context):
            context.chat_data['game_info']['budget'] = update.message.text
            update.message.reply_text('Введите дату завершения регистрации (в формате ММ/ДД/ГГГГ HH:MM):')
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
                print('-----Created game data-----')
                print(data_from_db)
                print('----------')

                update.message.reply_text(f'Игра {data_from_db["name"]} создана! Ссылка на игру: https://t.me/sssssssssannnttaaaa_bot?start={data_from_db["id"]}')
                return ConversationHandler.END
            except Exception as e:
                print(f"Error in create_game function: {e}")
                return ConversationHandler.END

        def register_user(update, context, game_id):
            context.user_data['game_id'] = game_id
            update.message.reply_text("Давайте начнем регистрацию. Пожалуйста, введите ваше имя:")
            return 'GET_NAME'

        def get_name(update, context):
            context.user_data['name'] = update.message.text
            update.message.reply_text("Теперь введите вашу фамилию:")
            return 'GET_LAST_NAME'

        def get_last_name(update, context):
            context.user_data['last_name'] = update.message.text
            update.message.reply_text("Поделитесь вашим номером телефона:")
            return 'GET_PHONE_NUMBER'

        def get_phone_number(update, context):
            context.user_data['phone'] = update.message.contact.phone_number if update.message.contact else update.message.text
            update.message.reply_text("Что бы вы хотели получить в подарок?")
            return 'CREATE_USER'
        

        def create_user(update, context):
            context.user_data['wishes'] = update.message.text
            user_info = context.user_data
            print(user_info)
            try:
                django_view_url = f'http://127.0.0.1:8000/create_user/'
                response = requests.post(django_view_url, json={
                    'tg_id': str(user_info['user_tg_id']),
                    'first_name': user_info['name'],
                    'last_name': user_info['last_name'],
                    'phone': user_info['phone'],
                    'is_admin': False,
                    'wishes': user_info['wishes'],
                    'game': user_info['game_id']
                    }
                )
                print(f"Sent POST request to Django for creating user: {user_info}")
                print(f"Response from Django: {response.text}")

                data_from_db = response.json()
                print('-----Created player data-----')
                print(data_from_db)
                print('----------')

                update.message.reply_text(f'Вы успешно зарегистрировались в игре!')
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
                'GET_NAME': [MessageHandler(Filters.text & ~Filters.command, get_name)],
                'GET_LAST_NAME': [MessageHandler(Filters.text & ~Filters.command, get_last_name)],
                'GET_PHONE_NUMBER': [MessageHandler(Filters.text & ~Filters.command, get_phone_number)],
                'CREATE_USER': [MessageHandler(Filters.text & ~Filters.command, create_user)],
            },
            fallbacks=[],
        )
        dispatcher.add_handler(conv_handler)

        updater.start_polling()
        updater.idle()
