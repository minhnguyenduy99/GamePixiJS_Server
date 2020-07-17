from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from ..serializers import GameStateSerializer, GameState, RetrieveGameStateSerializer, MapSerializer, GameStateMapSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from .permissions import UserPermission
from ..models import Map
from rest_framework.authentication import TokenAuthentication

class GameStateViewSet(viewsets.ModelViewSet):
  queryset = GameState.objects.all()
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated, UserPermission]
  page_size = 6

  def get_permissions(self):
    if self.action == 'create':
      self.permission_classes = [IsAuthenticated]
    return [permission() for permission in self.permission_classes]

  def get_queryset(self):
    user_id = self.request.auth.user.id
    return GameState.objects.filter(user=user_id)

  def perform_create(self, serializer):
    serializer.save(created_by=serializer.validated_data['user'].id)

  def get_serializer_class(self):
    if self.action in ['retrieve', 'list']:
      return RetrieveGameStateSerializer
    if self.action in ['by_user']:
      return GameStateMapSerializer
    return GameStateSerializer

  @action(detail=False, methods=['get'])
  def by_user(self, request, pk=None):
    page = request.query_params.get('page', 1)
    page = int(page)
    offset = (page - 1) * self.page_size
    # states = self.get_queryset()
    # serializer = self.get_serializer_class()(states, many=True)
    # return Response(serializer.data, status=status.HTTP_200_OK)
    listMaps = Map.objects.all()[offset:self.page_size]
    for map in listMaps:
      state = self.get_queryset().filter(game_map=map.id)[:1]
      if len(state) == 0:
        map.game_state = None
      else:
        map.game_state = state[0]
    return Response(GameStateMapSerializer(instance=listMaps, many=True).data, status=status.HTTP_200_OK)


  @action(detail=True, methods=['put'])
  def update_state(self, request, pk=None):
    game_state = self.get_object()
    if game_state.user.id != request.auth.user.id:
      error = {
        'error': 'Game state does not exist'
      }
      return Response(JSONParser().parse(error), status=status.HTTP_400_BAD_REQUEST)
    serializer = self.get_serializer_class()(instance=game_state, many=False, data=request.data, partial=True)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=status.HTTP_200_OK)
