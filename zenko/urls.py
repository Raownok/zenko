"""
URL configuration for zenko project.

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
from django.contrib import admin
from django.urls import path,include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from zenko import settings

from home import views
from cart import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('shop/', include('home.urls')),
    path('about/', include('home.urls')),
    path('shop/', include('home.urls')),
    path('perfume/', include('home.urls')),
    path('search/', include('home.urls')),
    path('product/', include('home.urls')),
    path('home/', include('home.urls')),
    path('about/', include('home.urls')),
    path('contact/', include('home.urls')),
    path('authenticate/', include('Authentication.urls')),
    #path('authenticate/', include('Authentication.urls')),
    path('cart/', include('home.urls')),
    path('accounts/', include('allauth.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
    
    
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
