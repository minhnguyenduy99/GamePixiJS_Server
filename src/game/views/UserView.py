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
      return Response(serialized_user.errors, status=status.HTTP_400_BAD_REQUEST)
    user = serialized_user.save()
    
    # Create profile of user
    data = serialized_user.data
    profile_keys = ['given_name', 'family_name', 'picture', 'picture_large']
    profile_data = {key:request.data.get(key, None) for key in profile_keys}
    profile_data['user'] = user.id

    serialized_profile = ProfileSerializer(data=profile_data)
    if not serialized_profile.is_valid():
      user.delete()
      return Response(serialized_profile.errors, status=status.HTTP_400_BAD_REQUEST)

    serialized_profile.save()
    token = {
      'access_token': generate_access_token(user),
      'refresh_token': generate_refresh_token(user)
    }
    data['token'] = token
    data['profile'] = serialized_profile.data

    return Response(data=data, status=status.HTTP_201_CREATED)


  @action(detail=False, methods=['POST'], url_path='/social/', permission_classes=[])
  def create_by_social(self, request):
    try:
      # If the user already exists
      profile = Profile.objects.get(social_id=request.data.get('social_id'))
      profileSerializer = RetrieveUserProfileSerializer(instance=profile, many=False)
      return Response(profileSerializer.data, status=status.HTTP_200_OK)
    except Profile.DoesNotExist:
      # Else
      success, dataOrError = self.transformAccountData(request.data)
      if success is not True:
        error = {
          'errors': dataOrError.args 
        }
        return Response(error, status=status.HTTP_400_BAD_REQUEST, content_type='application/json')
      serializer = CreateUserProfileSerializer(data=dataOrError)
      if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


  # @action(detail=True, methods=['PUT'])
  # def update(self, request, pk=None):
  #   user = User.objects.filter(profile__id=pk).first()
  #   if user is None:
  #     return Response(status=status.HTTP_404_NOT_FOUND)
  #   user = queryset[0]
  #   userSerializer = self.get_serializer_class()(instance=user, data=request.data, partial=True)
  #   if userSerializer.is_valid():
  #     userSerializer.save()
  #     return Response(userSerializer.data, status=status.HTTP_200_OK)
  #   return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


  def transformAccountData(self, data):
    user = data.get('user')
    if user is None:
      return False, ValueError('User cannot be null')
    user['username'] = data['social_id']
    email = user.get('email')
    if email is None:
      user['password'] = str(uuid.uuid1())
    else:
      user['password'] = email + str(uuid.uuid1())
    return True, data