from rest_framework.serializers import ModelSerializer
from ..models import Profile
from .UserSerializer import UserSerializer
from rest_framework.authtoken.models import Token


class CreateUserProfileSerializer(ModelSerializer):
  user = UserSerializer(many=False)

  class Meta:
    model = Profile
    fields = '__all__'

  
  def create(self, validated_data):
    user = validated_data.pop('user')
    userSerializer = UserSerializer(data=user)
    userSerializer.is_valid()
    userModel = userSerializer.save()
    token = Token.objects.get(user = userModel)
    userModel.token = token
    profile = Profile.objects.create(user=userModel, **validated_data)
    profile.save()
    return profile


class RetrieveUserProfileSerializer(ModelSerializer):
  user = UserSerializer(many=False, read_only=True)

  class Meta:
    model = Profile
    fields = '__all__'