from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Profile(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  social_id = models.CharField(max_length=200, unique=True)
  family_name = models.CharField(max_length=50, null=True)
  given_name = models.CharField(max_length=50, null=True)
  picture = models.URLField(null=True)
  picture_large = models.URLField(null=True)


@receiver(post_save, sender=User)
def create_user_token(sender, instance, created, **kwargs):
  if created:
    Token.objects.create(user=instance)
