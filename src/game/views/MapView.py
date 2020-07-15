from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication, TokenAuthentication
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.filters import OrderingFilter
from rest_framework.decorators import action
from ..serializers import MapSerializer, Map
from .permissions import UserPermission
from .pagination import SmallPagination

class MapViewSet(viewsets.ModelViewSet):
  queryset = Map.objects.all().order_by('-last_edited')
  serializer_class = MapSerializer
  pagination_class = SmallPagination
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated, UserPermission]

  def perform_create(self, serializer):
    serializer.save(created_by=self.request.auth.user.id)


