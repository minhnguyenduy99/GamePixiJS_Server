from rest_framework import serializers
from ..models import GameState, Map
from .MapSerializer import MapSerializer

class GameStateSerializer(serializers.ModelSerializer):
  class Meta:
    model = GameState
    fields = '__all__'
    read_only_fields = ['created_by']


class RetrieveGameStateSerializer(serializers.ModelSerializer):
  game_map = MapSerializer(read_only=True)

  class Meta:
    model = GameState
    fields = '__all__'