from .models import Game
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
import json

@csrf_exempt
def create_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            #date = datetime.strptime(data.get('draw_date'), '%m/%d/%Y')

            Game.objects.create(
                name=data.get('name'),
                is_limited=data.get('is_limited'),
                budget=data.get('budget'),
                #draw_date=datetime(date.year,date.month,date.day,tzinfo=None),#datetime.strptime(data.get('draw_date'), '%m/%d/%Y'),
                
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
