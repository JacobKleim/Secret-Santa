import json
from datetime import datetime, timedelta

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.timezone import make_aware

from app.forms import Registration_Form
from app.models import Game, Player


@csrf_exempt
def create_game(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            draw_date = make_aware(datetime.strptime(data.get('draw_date'), '%m/%d/%Y %H:%M'))

            game_name = data.get('game_name')

            send_date = draw_date + timedelta(days=3)
            response_data = {'status': 'success',
                             'message': f'Игра "{game_name}" создана!'}
            Game.objects.create(
                name=data.get('name'),
                is_limited=data.get('is_limited'),
                budget=data.get('budget'),
                draw_date=draw_date,
                send_date=send_date

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
            print(data)
            Player.objects.create(
                first_name=data.get('first_name'),
                last_name=data.get('last_name'),
                tg_id=data.get('tg_id'),                
                phone=data.get('phone'),
                is_admin=data.get('is_admin'),
                wishes=data.get('wishes')).games.add(Game.objects.get(pk=int(data.get('game')))
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
            return JsonResponse(
                {'status': 'error',
                 'message': 'Invalid JSON format in the request'})


@csrf_exempt
def registration(request):
    if request.method == "POST":
        form = Registration_Form(request.POST)

        if form.is_valid():
            game = form.cleaned_data['game']
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            phone = form.cleaned_data['phone']
            email = form.cleaned_data['email']
            wishes = form.cleaned_data['wishes']
            existing_player = Player.objects.filter(
                email=email,
                game=game).first()
            if existing_player:
                return render(request,
                              'base.html',
                              {'form': form,
                               'error_message': 'Вы уже зарегистрированы!'})
            else:
                try:
                    Player.objects.create(
                        game=game,
                        first_name=first_name,
                        last_name=last_name,
                        phone=phone,
                        email=email,
                        wishes=wishes)
                    success_message = (
                        f'Превосходно, ты в игре! '
                        f'{game.draw_date.date()} мы проведем жеребьевку '
                        'и ты узнаешь имя и контакты своего тайного друга. '
                        'Ему и нужно будет подарить подарок!')
                    return render(request, 'base.html',
                                  {'success_message': success_message})
                except Exception as e:
                    return HttpResponse(f'Ошибка: {e}')

    form = Registration_Form()
    return render(request, 'base.html', {'form': form})
