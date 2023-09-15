from django.contrib import admin
from .models import UploadedImage

# UploadedImageモデルをadminサイトに登録
admin.site.register(UploadedImage)