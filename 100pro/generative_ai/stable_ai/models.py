from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='masking/',blank=True, null=True)
    mask = models.ImageField(upload_to='masking/',blank=True, null=True)