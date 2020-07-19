from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import NotFound
from rest_framework.permissions import SAFE_METHODS
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from ..models import Map
from ..permissions import GameStateOwnPermission
from ..serializers import GameStateSerializer, RetrieveGameStateSerializer, GameState
from .pagination import SmallPagination

class GameStateViewSet(viewsets.ModelViewSet):
  queryset = GameState.objects.all()
  serializer_class = GameStateSerializer
  permission_classes = [IsAuthenticated, GameStateOwnPermission]
  pagination_class = SmallPagination
  pagination_class.page_size = 6

  def get_serializer_class(self):
    if self.request.method in SAFE_METHODS:
      self.serializer_class = RetrieveGameStateSerializer
    else:
      self.serializer_class = GameStateSerializer
    return self.serializer_class

  def get_permissions(self):
    if self.action == 'create':
      self.permission_classes = [IsAuthenticated]
    return [permission() for permission in self.permission_classes]

  def get_queryset(self):
    user_id = self.request.user.id
    self.queryset = GameState.objects.filter(user=user_id).order_by('-saved_date')
    return self.queryset

  def get_user(self):
    User = get_user_model()
    user = User.objects.filter(id=self.request.data.get('user', None)).first()
    if user is None:
      raise NotFound('The user is not found')
    return user

  def get_map(self):
    requested_map = self.request.data.get('game_map', None)
    map = Map.objects.filter(id = requested_map).first()
    if map is None:
      raise NotFound('The map is not found')
    return map

  
  def create(self, request):
    user = self.get_user()
    map = self.get_map()
    state = GameState.objects.filter(user=user.id, game_map=map.id).first()
    if state is not None:
      return Response({ 'error': 'The state already exists'}, status=status.HTTP_400_BAD_REQUEST)
    serialized_gamestate = self.get_serializer_class()(data=request.data)
    if serialized_gamestate.is_valid():
      serialized_gamestate.save()
      return Response(serialized_gamestate.data, status=status.HTTP_201_CREATED)
    return Response(serialized_gamestate.errors, status=status.HTTP_400_BAD_REQUEST)

  def update(self, request, pk=None):
    game_state = self.get_object()
    serializer = self.get_serializer_class()(instance=game_state, many=False, data={ 'state': request.data.get('state', None)}, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
