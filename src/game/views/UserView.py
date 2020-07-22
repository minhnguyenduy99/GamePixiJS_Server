import uuid
import json
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.decorators import action, authentication_classes, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from .TokenView import generate_access_token, generate_refresh_token
from ..permissions import UserOwnPermission
from ..serializers import (
  UserSerializer,
  CreateUserSerializer,
  UpdateUserSerializer,
  User,
  Profile,
  ProfileSerializer,
  UpdateUserSerializer,
  ProfileSerializer
)

class UserViewSet(
  mixins.CreateModelMixin,
  mixins.RetrieveModelMixin,
  mixins.ListModelMixin,
  mixins.UpdateModelMixin,
  viewsets.GenericViewSet):

  queryset = User.objects.all()
  pagination_class = PageNumberPagination
  pagination_class.page_size = 5
  filter_backends = [SearchFilter]
  search_fields = ['=family_name', '=given_name']
  permission_classes = [IsAuthenticated, UserOwnPermission]

  serializer_classes = {
    'create': CreateUserSerializer,
    'retrieve': UserSerializer,
    'update': UpdateUserSerializer,
    'update_account': UpdateUserSerializer,
    'update_profile': ProfileSerializer,
    'list': ProfileSerializer
  }

  def get_serializer_class(self):
    return self.serializer_classes.get(self.action, None)

  def get_permissions(self):
    if self.request.method == 'POST':
      return []
    return [permission() for permission in self.permission_classes]

  def create(self, request):
    # create user
    serialized_user = self.get_serializer_class()(data=request.data)
    
    if not serialized_user.is_valid():
      error = [serialized_user.errors[key][0] for key in serialized_user.errors]
      return Response({ 'error': error[0] }, status=status.HTTP_400_BAD_REQUEST)
    user = serialized_user.save()
    
    # Create profile of user
    data = serialized_user.data
    profile_keys = ['given_name', 'family_name', 'picture', 'picture_large']
    profile_data = {key:request.data.get(key, None) for key in profile_keys}
    profile_data['user'] = user.id

    serialized_profile = ProfileSerializer(data=profile_data)
    if not serialized_profile.is_valid():
      user.delete()
      error = [serialized_profile.errors[key][0] for key in serialized_profile.errors]
      return Response({ 'error': error[0] }, status=status.HTTP_400_BAD_REQUEST)

    serialized_profile.save()
    token = {
      'access_token': generate_access_token(user),
      'refresh_token': generate_refresh_token(user)
    }
    data['token'] = token
    data['profile'] = serialized_profile.data

    return Response(data=data, status=status.HTTP_201_CREATED)


  def get_social_user(self, request):
    # If the user already exists
    profile = Profile.objects.get(social_id=request.data.get('social_id'))
    user = User.objects.get(id=profile.user.id)
    user_data = UserSerializer(instance=user).data
    profile_data = ProfileSerializer(instance=profile).data
    user_data['profile'] = profile_data
    token = {
      'access_token': generate_access_token(user),
      'refresh_token': generate_refresh_token(user)
    }
    data['token'] = token
    return data


  @action(detail=True, methods=['PUT'], url_path='profile')
  def update_profile(self, request, pk=None):
    profile = Profile.objects.filter(user=pk).first()
    if profile is None:
      return Response({ 'error': 'Profile not found'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    serialized_profile = self.get_serializer_class()(instance=profile, data=request.data, partial=True)
    if serialized_profile.is_valid():
      serialized_profile.save()
      return Response(serialized_profile.data, status=status.HTTP_200_OK)
    return Response(serialized_profile.errors, status=status.HTTP_400_BAD_REQUEST)