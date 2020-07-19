from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
from django.contrib.auth.models import User
from django.conf import settings

import jwt

class JWTAuthentication(BaseAuthentication):

  def authenticate(self, request):
    authenticate = request.headers.get('Authorization')

    if not authenticate:
      return None
    try:
      token = authenticate.split(' ')[1]
      payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise exceptions.AuthenticationFailed('The token has been expired')
    except (IndexError, jwt.DecodeError):
      raise exceptions.AuthenticationFailed('Token has invalid format')
    
    user = User.objects.filter(id=payload['user_id']).first()
    if user is None:
      raise exceptions.AuthenticationFailed('User not found')
      
    if not user.is_active:
      raise exceptions.AuthenticationFailed('User is inactive')

    return (user, None)
      