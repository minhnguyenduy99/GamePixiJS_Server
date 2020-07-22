import uuid
from rest_framework.serializers import *
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .ProfileSerializer import ProfileSerializer
from ..models import Profile


class UserSerializer(ModelSerializer):
  profile = ProfileSerializer()

  class Meta:
    model = User
    fields = ['id', 'username', 'password', 'email', 'profile']
    extra_kwargs = {'password': {'write_only': True}}

  def get_profile(self, obj):
    profile = Profile.objects.filter(user=obj.id).first()
    return profile


class CreateUserSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['id', 'username', 'password', 'email']
    extra_kwargs = {'password': {'write_only': True}}

  def save(self):
    user = super().save()
    user.set_password(user.password)
    user.save()
    return user


class CreateUserFromSocialSerializer(ModelSerializer):
  class Meta:
    model = User
    fields = ['id']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    data = kwargs['data']
    if data is None:
      return
    data['username'] = uuid.uuid1()
    data['password'] = uuid.uuid1()


class UpdateUserSerializer(ModelSerializer):

  class Meta:
    model = User
    fields = ['id', 'username', 'password']
    extra_kwargs = {'password': {'write_only': True}}
    read_only_fields = ['id', 'email']

  def validate_username(self, value):
    return value

  def update(self, instance, validated_data):
    self.is_valid()
    instance.username = validated_data.get('username', instance.username)
    password = validated_data.get('password')
    if password is not None:
      instance.set_password(validated_data.get('password'))
    instance.save()
    return instance