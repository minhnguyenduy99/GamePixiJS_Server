from rest_framework import serializers
from ..models import GameState, Map
from .MapSerializer import MapSerializer

class GameStateSerializer(serializers.ModelSerializer):
  class Meta:
    model = GameState
    fields = '__all__'
    read_only_fields = ['created_by']


class RetrieveGameStateSerializer(serializers.ModelSerializer):
  game_map = MapSerializer(read_only=True, default=None)

  class Meta:
    model = GameState
    fields = '__all__'



class GameStateMapSerializer(serializers.ModelSerializer):
  game_state = GameStateSerializer(default=None, required=False)

  class Meta:
    model=Map
    fields = '__all__'