import os
import telegram
from dotenv import load_dotenv


def main():
    load_dotenv()
    token = os.environ["TG_TOKEN"]
    bot = telegram.Bot(token=token)
    chat_id = 275657147
    message_text = 'Привет! Это тестовое сообщение от бота.'
    bot.send_message(chat_id=chat_id, text=message_text)


if __name__ == '__main__':
    main()
