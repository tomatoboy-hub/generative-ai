from django.db import models

# Create your models here.
class Image(models.Model):
    image = models.ImageField(upload_to='masking/',blank=True, null=True)
    mask = models.ImageField(upload_to='masking/',blank=True, null=True)
class UploadedImage(models.Model):
    image = models.ImageField(upload_to='uploaded_images/')
