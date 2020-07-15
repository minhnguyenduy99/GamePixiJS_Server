from django.contrib.auth.models import User
from django.db import models
from .Map import Map

class GameState(models.Model):
  game_map = models.ForeignKey(Map, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  saved_date = models.DateField(auto_now=True)
  created_by = models.CharField(max_length=200)