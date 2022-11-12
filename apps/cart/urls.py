from django.urls import path

from apps.cart.views import cart_detail, success

urlpatterns = [
    path('', cart_detail, name='cart'),
    path('success/', success, name='success')
]