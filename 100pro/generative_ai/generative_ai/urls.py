"""
URL configuration for generative_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.conf import settings
# from django.conf.urls.static import static


# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('', include('stable_ai.urls')),
# ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from stable_ai import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('', views.index, name='index'),
    path('im2im/', views.im2im, name='im2im'),    
    path('generated/', views.generated, name='generated'),    
    path('images/', views.image_list, name='image_list'),
    path('upload/', views.upload_image, name='upload_image'),
    path('txtotx/', views.txtotx, name='txtotx'),
    path('txtoim/', views.txtoim, name='txtoim'),
    path('images/delete/<int:image_id>/', views.delete_image, name='delete_image'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)