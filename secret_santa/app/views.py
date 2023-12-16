from .models import Game, Player
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from django.utils.timezone import make_aware
import json

@csrf_exempt
def create_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            date = make_aware(datetime.strptime(data.get('draw_date'), '%m/%d/%Y %H:%M'))

            Game.objects.create(
                name=data.get('name'),
                is_limited=data.get('is_limited'),
                budget=data.get('budget'),
                draw_date=date,#datetime(date.year,date.month,date.day,tzinfo=),#datetime.strptime(data.get('draw_date'), '%m/%d/%Y'),
                is_drawn=False
            )
            created_game = Game.objects.last()
            response_data = {
                'status': 'success',
                'id': created_game.id,
                'name': created_game.name,
                'is_limited': created_game.is_limited,
                'budget': created_game.budget,
                'draw_date': created_game.draw_date
            }
            return JsonResponse(response_data)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in the request'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


@csrf_exempt
def create_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))

            Player.objects.create(
                tg_id=data.get('tg_id'),
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                phone=data.get('phone'),
                is_admin=data.get('is_admin'),
                wishes=data.get('wishes'),
            )
            created_user = Player.objects.last()
            response_data = {
                'status': 'success',
                'tg_id': created_user.tg_id,
                'first_name': created_user.first_name,
                'last_name': created_user.last_name,
                'phone': created_user.phone,
                'wishes': created_user.wishes
            }
            return JsonResponse(response_data)
        except json.decoder.JSONDecodeError:
            return JsonResponse({'status': 'error', 'message': 'Invalid JSON format in the request'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})
