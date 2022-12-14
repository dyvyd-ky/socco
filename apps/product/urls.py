from django.urls import path

from . import views
from .api import *

urlpatterns = [
    path('search/', views.search, name='search'),
    
    #api
    path('api/add_to_cart/', api_add_to_cart, name='api_add_to_cart'),
    path('api/remove_from_cart/', api_remove_from_cart, name='api_remove_from_cart'),
    path('api/create_checkout_session/', create_checkout_session, name='create_checkout_session'),
    path('<slug:category_slug>/<slug:product_slug>/', views.product, name='product'),
    path('<slug:category_slug>/', views.category, name='category'),
    
]