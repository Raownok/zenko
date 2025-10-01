from django.contrib import admin
from django.urls import path

from django.conf import settings
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from zenko import settings

from . import views


urlpatterns = [
    path('',views.home,name = 'home'),
    path('view/',views.shop, name = 'shop'),
    path("product/<int:pk>/",views.viewProduct , name = 'viewProduct'),
    path("<int:pk>/",views.viewFeaturedProduct , name = 'viewFeaturedProduct'),
    # Search
    path("search_Result/",views.searchResult , name = 'search-Result'),
    path("suggest/", views.search_suggest, name="search_suggest"),
    path("cleanserAndFacewash/",views.cleanserAndFacewash , name = 'cleanserAndFacewash'),
    path("toner/",views.toner , name = 'toner'),
    path("makeup/",views.makeup , name = 'makeup'),
    path("scerum/",views.scerum , name = 'scerum'),
    path("moisturizer/",views.moisturizer , name = 'moisturizer'),
    path("sunscreen/",views.sunscreen , name = 'sunscreen'),
    path("aboutPage/", views.about, name = "about"),
    path("male/", views.male_Perfume, name = "male_Perfume"),
    path("female/", views.female_Perfume, name = "female_Perfume"),
    path("unisex/", views.unisex_Perfume, name = "unisex_Perfume"),
    path("contactPage/", views.contact, name = "contact"),
    # Cart URLs
    # Cart URLs
    path('cart/', views.view_cart, name='view_cart'),
    path('cart/add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('buy-now/<int:product_id>/', views.buy_now, name='buy_now'),
    path('profile/', views.profile, name='profile'),
    path('cart/ajax/add/<int:item_id>/', views.ajax_add_to_cart, name='ajax_add_to_cart'),
    path('cart/ajax/remove/<int:item_id>/', views.ajax_remove_from_cart, name='ajax_remove_from_cart'),

    path('checkout/', views.checkout, name='place_order'),
    path('place-order/', views.place_order, name='place_order'),
    path('thank-you/', views.thank_you, name='thank_you'),
    path('checkout/', views.checkout, name='checkout'), 
    # Export
    path('profile/orders.pdf', views.profile_orders_pdf, name='profile_orders_pdf'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
