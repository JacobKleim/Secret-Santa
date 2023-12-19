from django.contrib import admin

from .models import DrawingResult, Game, Player


class PlayerInline(admin.TabularInline):
    model = Player.games.through
    extra = 1


@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    inlines = [PlayerInline]


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    pass


@admin.register(DrawingResult)
class DrawingResultAdmin(admin.ModelAdmin):
    pass
