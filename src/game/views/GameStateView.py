from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action, permission_classes
from ..serializers import GameStateSerializer, GameState, RetrieveGameStateSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import UserPermission
from rest_framework.authentication import TokenAuthentication

class GameStateViewSet(viewsets.ModelViewSet):
  queryset = GameState.objects.all()
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAuthenticated, UserPermission]

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
    if self.action in ['retrieve', 'list', 'by_user']:
      return RetrieveGameStateSerializer
    return GameStateSerializer

  @action(detail=False, methods=['get'], url_path='by_user/(?P<user_id>[a-zA-Z0-9]+)')
  def by_user(self, request, pk=None, user_id=None):
    states = self.get_queryset()
    serializer = self.get_serializer_class()(states, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)