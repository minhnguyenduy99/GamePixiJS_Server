from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.generics import GenericAPIView
from rest_framework import exceptions
from rest_framework.response import Response
from django.conf import settings
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
import jwt
import datetime

def generate_access_token(user):
  access_token_payload = {
    'user_id': user.id,
    'exp': datetime.datetime.now() + datetime.timedelta(days=0, minutes=5),
    'iat': datetime.datetime.now()
  }
  access_token = jwt.encode(access_token_payload, settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

  return access_token


def generate_refresh_token(user):
  refresh_token_payload = {
    'user_id': user.id,
    'exp': datetime.datetime.now() + datetime.timedelta(days=7),
    'iat': datetime.datetime.now()
  }
  refresh_token = jwt.encode(refresh_token_payload, settings.REFRESH_TOKEN_SECRET_KEY, algorithm='HS256').decode('utf-8')

  return refresh_token




@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
@csrf_protect
def get_access_token(request):
  '''
  To obtain a new access_token this view expects 2 important things:
      1. a cookie that contains a valid refresh_token
      2. a header 'X-CSRFTOKEN' with a valid csrf token, client app can get it from cookies "csrftoken"
  '''
  User = get_user_model()
  refresh_token = request.COOKIES.get('refresh_token')

  if refresh_token is None:
    raise exceptions.AuthenticationFailed('Authentication credentials were not provided')

  try:
    payload = jwt.decode(refresh_token, settings.REFRESH_TOKEN_SECRET_KEY)
  except jwt.ExpiredSignatureError:
    raise exceptions.AuthenticationFailed('The refresh token is expired. Please login again')
  except jwt.InvalidTokenError:
    raise exceptions.AuthenticationFailed('The refresh token is invalid')

  user = User.objects.filter(id=payload.get('user_id')).first()
  if user is None:
    raise exceptions.AuthenticationFailed('User not found')

  if not user.is_active:
    raise exceptions.AuthenticationFailed('User is inactive')

  access_token = generate_access_token(user)
  return Response({'token': access_token})

  
  