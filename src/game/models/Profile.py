from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  social_id = models.CharField(max_length=200, unique=True, null=True)
  family_name = models.CharField(max_length=50, null=True)
  given_name = models.CharField(max_length=50, null=True)
  picture = models.URLField(null=True)
  picture_large = models.URLField(null=True)