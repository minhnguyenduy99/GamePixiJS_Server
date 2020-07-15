from rest_framework.serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User


class UserSerializer(ModelSerializer):
  token = SerializerMethodField()

  class Meta:
    model = User
    fields = ['id', 'username', 'password', 'email', 'token']
    extra_kwargs = {'password': {'write_only': True}}

  def get_token(self, obj):
    token = Token.objects.get(user=obj.id)
    return token.key



class UpdateUserSerializer(ModelSerializer):

  class Meta:
    model = User
    fields = ['id', 'username', 'password', 'email']
    extra_kwargs = {'password': {'write_only': True}}
    read_only_fields = ['id', 'email']

  def validate_username(self, value):
    return value

  def update(self, instance, validated_data):
    instance.username = validated_data.get('username', instance.username)
    password = validated_data.get('password')
    if password is not None:
      instance.set_password(validated_data.get('password'))
    instance.save()
    return instance