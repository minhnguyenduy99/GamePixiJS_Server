from rest_framework import serializers
from ..models import GameState, Map
from .MapSerializer import MapSerializer

class RetrieveGameStateSerializer(serializers.ModelSerializer):
  game_map = MapSerializer(required=False)

  class Meta:
    model = GameState
    fields = '__all__'
 

class GameStateSerializer(serializers.ModelSerializer):
  class Meta:
    model = GameState
    fields = '__all__'