from django.urls import path

from app.views import create_game, registration

urlpatterns = [
    path('create_game/', create_game, name='create_game'),
    path('registration/', registration, name='registration'),
]
