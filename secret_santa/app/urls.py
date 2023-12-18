from django.urls import path

from app.views import create_game, registration

urlpatterns = [
    path('create_game/', create_game, name='create_game'),
    path('create_user/', create_game, name='create_user'),
    path('registration/', registration, name='registration'),
]
