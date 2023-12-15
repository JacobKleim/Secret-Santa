from django import forms

from app.models import Game, Player


class GameChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        game = (f'Название игры: {obj.name}, Бюджет: {obj.budget}, '
                f'Дата жеребьевки: {obj.draw_date}, '
                f'Дата отправки подарков после: {obj.send_date}')
        return game


class Registration_Form(forms.ModelForm):
    game = GameChoiceField(
        queryset=Game.objects.all(),
        label='Выберите игру'
    )

    class Meta:
        model = Player
        fields = ['first_name',
                  'last_name',
                  'phone',
                  'email',
                  'wishes',
                  'game']
