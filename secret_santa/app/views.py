from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import Game
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def create_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            game_name = data.get('game_name')

            # Выполните необходимые действия с игрой
            Game.objects.create(name=game_name)

            # Вернем JSON-ответ, чтобы бот мог получить результат
            response_data = {'status': 'success', 'message': f'Игра "{game_name}" создана!'}
            return JsonResponse(response_data)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in the request'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
