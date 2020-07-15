import uuid
import json
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, status, mixins
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser, JSONParser
from rest_framework.decorators import action, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import SearchFilter

from ..serializers import (
  UserSerializer,
  UpdateUserSerializer,
  User,
  RetrieveUserProfileSerializer,
  Profile,
  ProfileSerializer,
  CreateUserProfileSerializer,
  UpdateUserSerializer,
  ProfileSerializer
)

class UserViewSet(
  mixins.CreateModelMixin,
  mixins.RetrieveModelMixin,
  mixins.ListModelMixin,
  mixins.UpdateModelMixin,
  viewsets.GenericViewSet):

  queryset = Profile.objects.all()
  pagination_class = PageNumberPagination
  pagination_class.page_size = 5
  filter_backends = [SearchFilter]
  search_fields = ['=family_name', '=given_name']

  serializer_classes = {
    'create': CreateUserProfileSerializer,
    'retrieve': RetrieveUserProfileSerializer,
    'update': ProfileSerializer,
    'update_account': UpdateUserSerializer,
    'list': ProfileSerializer
  }

  def get_serializer_class(self):
    return self.serializer_classes.get(self.action, None)

  def create(self, request):
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


  @action(detail=True, methods=['PUT'])
  def update_account(self, request, pk=None):
    try:
      queryset = User.objects.filter(profile__id=pk)[0:1]
      if queryset.count() == 0:
        return Response(status=status.HTTP_404_NOT_FOUND)
    except ValueError as e:
      errors = {
        'errors': e.args
      }
      return Response(errors, status=status.HTTP_400_BAD_REQUEST)
    user = queryset[0]
    userSerializer = self.get_serializer_class()(instance=user, data=request.data, partial=True)
    if userSerializer.is_valid():
      userSerializer.save()
      return Response(userSerializer.data, status=status.HTTP_200_OK)
    return Response(userSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


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