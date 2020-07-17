from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from ..serializers import MapSerializer, Map
from .permissions import UserPermission
from .pagination import SmallPagination
from ..services import FileUploader

class MapViewSet(viewsets.ModelViewSet):
  queryset = Map.objects.all().order_by('-last_edited')
  serializer_class = MapSerializer
  pagination_class = SmallPagination
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated]

  def perform_create(self, serializer):
    serializer.save(created_by=self.request.auth.user.id)


  def create(self, request):
    map_image = request.data.get('map_image', None)
    map_file = request.data.get('map_file', None)
    if map_file is None or map_image is None:
      data = {
        'error': 'Image and map file are required'
      }
      return Response(JSONParser().parse(data) ,status=status.HTTP_400_BAD_REQUEST)
    results = [FileUploader.uploadFile(file) for file in (map_image, map_file)]
    if results[0] is None or results[1] is None:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    request.data['map_image'] = results[0]
    request.data['map_file'] = results[1]
    mapSerializer = self.get_serializer_class()(data=request.data, many=False)
    if mapSerializer.is_valid():
      mapSerializer.save(created_by=self.request.auth.user.id)
      return Response(mapSerializer.data, status=status.HTTP_201_CREATED)
    return Response(mapSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


  def update(self, request, pk=None):
    map_image = request.data.get('map_image', None)
    map_file = request.data.get('map_file', None)
    if map_file is None or map_image is None:
      data = {
        'error': 'Image and map file are required'
      }
      return Response(JSONParser().parse(data) ,status=status.HTTP_400_BAD_REQUEST)
    results = [FileUploader.uploadFile(file) for file in (map_image, map_file)]
    if results[0] is None or results[1] is None:
      return Response(status=status.HTTP_400_BAD_REQUEST)
    request.data['map_image'] = results[0]
    request.data['map_file'] = results[1]
    mapSerializer = self.get_serializer_class()(instance = self.get_object(), data=request.data)
    if mapSerializer.is_valid():
      mapSerializer.save()
      return Response(mapSerializer.data, status=status.HTTP_200_OK)
    return Response(mapSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


