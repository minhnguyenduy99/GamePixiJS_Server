from django.db import models
from cloudinary.models import CloudinaryField

class CloudinaryFile(models.Model):
  file = CloudinaryField()