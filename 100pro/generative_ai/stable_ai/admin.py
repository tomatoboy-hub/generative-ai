from django.contrib import admin
from .models import SnsModel, UploadedImage
# Register your models here.
admin.site.register(SnsModel)
# UploadedImageモデルをadminサイトに登録
admin.site.register(UploadedImage)
