from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from zenko import settings

from cart import views

urlpatterns = [
   path('', views.cart_Summary, name = "cart_Summary"),
   # path('add/', views.cart_Add, name = "cart_Add"),
   # path('delete/', views.cart_Delete, name = "cart_Delete"),
   # path('update/', views.cart_Update, name = "cart_Update"),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)