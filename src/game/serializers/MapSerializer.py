from rest_framework.serializers import ModelSerializer
from ..models import Map

class MapSerializer(ModelSerializer):
  class Meta:
    model = Map
    fields = '__all__'
    read_only_fields = ['created_by', 'last_edited']