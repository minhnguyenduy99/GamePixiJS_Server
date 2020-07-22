from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, SAFE_METHODS
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from ..serializers import MapSerializer, Map
from .pagination import SmallPagination
from ..permissions import MapOwnerPermission
from ..services import FileUploader


class MapViewSet(viewsets.ModelViewSet):
  queryset = Map.objects.all().order_by('-last_edited')
  serializer_class = MapSerializer
  permission_classes = [IsAuthenticatedOrReadOnly, MapOwnerPermission]
  pagination_class = SmallPagination
  pagination_class.page_size = 3

  def get_permissions(self):
    if self.request.method in ('POST',) + SAFE_METHODS:
      return [IsAuthenticatedOrReadOnly()]
    return [permission() for permission in self.permission_classes]

  def get_queryset(self):
    if self.action in ['retrieve', 'list']:
      self.queryset = self.queryset.filter(created_by=self.request.user.id)
    return self.queryset


  def create(self, request):
    self.create_map_and_image_file(request)
    request.data['created_by'] = request.user.id
    mapSerializer = self.get_serializer_class()(data=request.data, many=False)
    if mapSerializer.is_valid():
      mapSerializer.save()
      return Response(mapSerializer.data, status=status.HTTP_201_CREATED)
    # delete the uploaded files
    FileUploader.deleteFile(request.data['map_image_id'])
    FileUploader.deleteFile(request.data['map_file_id'])
    return Response(mapSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


  def update(self, request, pk=None):
    map = self.get_object()
    self.create_map_and_image_file(request)
    request.data['created_by'] = map.created_by
    mapSerializer = self.get_serializer_class()(instance = map, data=request.data)
    if mapSerializer.is_valid():
      mapSerializer.save()
      return Response(mapSerializer.data, status=status.HTTP_200_OK)
    # delete the uploaded files
    FileUploader.deleteFile(request.data['map_image_id'])
    FileUploader.deleteFile(request.data['map_file_id'])
    return Response(mapSerializer.errors, status=status.HTTP_400_BAD_REQUEST)

  def create_map_and_image_file(self, request):
    image = self.create_file(request, 'map_image', 'map_image_id', 'map_image_url', 'map_image is required')
    file = self.create_file(request, 'map_file', 'map_file_id', 'map_file_url', 'map_file is required')

    data = request.data
    data.update(file)
    data.update(image)


  def create_file(self, request, requestField, idField, urlField, error = None):
    file = request.data.get(requestField, None)
    if file is None:
      data = {
        'error': error
      }
      return Response(JSONParser().parse(data) ,status=status.HTTP_400_BAD_REQUEST)
    result = FileUploader.uploadFile(file)
    returnedResult = {}
    returnedResult[idField] = result['id']
    returnedResult[urlField] = result['url']
    return returnedResult

  def delete_file(self, request, request_field, id_field):
    FileUploader.deleteFile()