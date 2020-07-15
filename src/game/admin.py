from django.contrib import admin

from .models import Map, GameState, Profile

# Register your models here.
admin.site.register(Map)
admin.site.register(GameState)
admin.site.register(Profile)