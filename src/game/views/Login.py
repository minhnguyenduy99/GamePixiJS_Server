from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework import exceptions
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_protect
from ..serializers import UserSerializer, User
from .TokenView import generate_access_token, generate_refresh_token

@api_view(['POST'])
@authentication_classes([])
@permission_classes([AllowAny])
@ensure_csrf_cookie
def login(request):
  username = request.data.get('username', None)
  password = request.data.get('password', None)

  user = User.objects.filter(username=username).first()
  if user is None:
    raise exceptions.AuthenticationFailed(detail='The username or password is incorrect')   
  passwordCorrect = user.check_password(password)
  if not passwordCorrect:
    raise exceptions.AuthenticationFailed(detail='The username or password is incorrect')
  
  user_serializer = UserSerializer(instance=user, many=False).data
  access_token = generate_access_token(user)
  refresh_token = generate_refresh_token(user)

  response = Response()

  response.set_cookie(key='refresh_token', value=refresh_token, httponly=True)
  response.data = {
    'access_token': access_token,
    'user': user_serializer
  }
  response.status_code = status.HTTP_200_OK
  return response


