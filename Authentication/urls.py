from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from zenko import settings

from Authentication import views

urlpatterns = [
    path('accounts/', include('allauth.urls')),
    path("signin/", views.signin, name='signin'),
    path("signup/", views.signup, name='signup'),
    path("signout/", views.signout, name='signout'),
    
    # Phone authentication URLs
    path("phone-login/", views.phone_login, name='phone_login'),
    
    # Admin login
    path("admin-login/", views.admin_login, name='admin_login'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)