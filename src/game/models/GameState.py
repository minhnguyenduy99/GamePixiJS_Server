from django.contrib.auth.models import User
from django.db import models
from .Map import Map

class GameState(models.Model):
  ARCHIEVED = 'AR'
  ONPROGRESS = 'OP'
  NOTARCHIEVED = 'NA'

  STATE_CHOICES = (
    (ARCHIEVED, 'archieved'),
    (ONPROGRESS, 'on_progress'),
    (NOTARCHIEVED, 'not_archieved')
  )
  game_map = models.ForeignKey(Map, on_delete=models.CASCADE)
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  saved_date = models.DateField(auto_now=True)
  state = models.CharField(max_length=20, choices=STATE_CHOICES, default=NOTARCHIEVED)

  class Meta:
    unique_together = ('user', 'game_map',)