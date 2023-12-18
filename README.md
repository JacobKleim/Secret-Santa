# Secret-Santa


Телеграм-бот для организации обмена подарками, написанный на Python с использованием библиотеки python-telegram-bot.
Бот позволяет пользователям создавать игру "Тайный Санта" и управлять ей через удобный интерфейс Telegram.

#### Использованные технологии:
![SQLite](https://img.shields.io/badge/sqlite-%2307405e.svg?style=for-the-badge&logo=sqlite&logoColor=white)
![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white)
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)


![License](https://img.shields.io/github/license/JacobKleim/Secret-Santa) 

## Установка проекта

Откройте терминал и создайте виртуальное окружение:
```python
python -m venv venv
```
Активируйте виртуальное окружение:
```python
source venv/Scripts/activate
```
Получите Телеграм-токен с помощью **@BotFather** в Телеграме.
Создайте файл .env и поместите туда токен:

```python 
TELEGRAM_TOKEN ="ваш_телеграм_токен"
```

Установите пакеты, необходимые для работы с проектом:
```python
pip install -r requirements.txt
```
## Запуск проекта


Для запуска проекта выполните следующую команду:
```python
python manage.py runserver
```
Для запуска бота выполните следующую команду:
```python
python manage.py bot
```
## Работа с ботом

Для начала игры необходимо открыть диалог с [ботом](https://t.me/SantsSecretSants_bot).
Если бота запускает администратор, он вызывает /start без дополнительных параметров. 
Если пользователь хочет зарегистрироваться на игру, он должен ввести /start и id игры.