from django.db import models

class Map(models.Model):
  map_name = models.CharField(max_length=200, blank=False, null=False)
  map_image = models.FileField(blank=False, null=False)
  map_file = models.FileField(blank=False, null=False)
  created_by = models.CharField(max_length=200)
  last_edited = models.DateTimeField(auto_now_add=True)