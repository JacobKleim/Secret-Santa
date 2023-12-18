# Secret-Santa

python -m venv venv

source venv/Scripts/activate

python -m pip install --upgrade pip

pip install -r requirements.txt

python manage.py makemigrations

python manage.py migrate

python manage.py createsuperuser

<!-- Для запуска проекта выполните следующую команду -->
python manage.py runserver

<!-- Для запуска бота выполните следующую команду -->
python manage.py bot