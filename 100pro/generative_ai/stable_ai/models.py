from django.db import models
file_name = 'miss'
def changePath(instance, filename):
    ext = filename.split('.')[-1]
    file_name = f'changed.{ext}'
    return file_name

  # Create your models here.
class SnsModel(models.Model):
    slug = models.SlugField(null=True)
    # title = models.CharField(max_length=100)
    content = models.TextField(max_length=100, null=True)
    image = models.ImageField(upload_to='',blank=True ,null=True) # upload_toはどこのディレクトリに画像をアップロードするかの設定
    file = models.FileField(upload_to=changePath,null=True,blank=True)
    # readtext = models.CharField(max_length=200)
    posted_date = models.DateTimeField(auto_now_add=True,blank=True ,null=True)
