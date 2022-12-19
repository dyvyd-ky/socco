from django.urls import path

from . import views
from .api import *

urlpatterns = [
    path('search/', views.search, name='search'),
    #path('daraja/stk-push/', stk_push_callback, name='mpesa_stk_push_callback'),
    #api

    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
    path('api/checkout/', index, name='checkout'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
    path('<slug:category_slug>/', views.category, name='category'),
    
]