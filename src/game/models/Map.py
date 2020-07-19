from django.db import models

class Map(models.Model):
  map_name = models.CharField(max_length=200, blank=False, null=False)
  map_image_id = models.CharField(max_length = 200, blank=False, null=False)
  map_file_id = models.CharField(max_length=200, blank=False, null=False)
  map_image_url = models.URLField(blank=False, null=False)
  map_file_url = models.URLField(blank=False, null=False)
  created_by = models.IntegerField(null=False, blank=False)
  last_edited = models.DateTimeField(auto_now_add=True)