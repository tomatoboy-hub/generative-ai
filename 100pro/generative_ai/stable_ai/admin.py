from django.contrib import admin
from .models import UploadedImage,SnsModel
# Register your models here.
admin.site.register(SnsModel)
# UploadedImageモデルをadminサイトに登録
admin.site.register(UploadedImage)
