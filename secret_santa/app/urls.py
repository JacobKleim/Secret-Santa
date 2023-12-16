from django.urls import path
from .views import create_game, create_user

urlpatterns = [
    path('create_game/', create_game, name='create_game'),
    path('create_user/', create_user, name='create_user'),

]
