from rest_framework.serializers import ModelSerializer
from ..models import Map
from ..services import FileUploader

class MapSerializer(ModelSerializer):
  class Meta:
    model = Map
    fields = '__all__'
    read_only_fields = ['id', 'last_edited']
    extra_kwargs = {
      'map_image_id': {'write_only': True},
      'map_file_id': {'write_only': True},
    }

    