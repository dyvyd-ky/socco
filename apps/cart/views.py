

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from .cart import Cart
from .forms import CheckoutForm

from apps.order.utilities import checkout, notify_customer, notify_vendor

def cart_detail(request):
    cart = Cart(request)
    productsstring = ''

    for item in cart:
        product = item['product']
        url = '/%s/%s/' % (product.category.slug, product.slug)
        b = "{'id': '%s', 'title': '%s', 'price': '%s', 'quantity': '%s', 'total_price': '%s', 'thumbnail': '%s', 'url': '%s', 'num_available': '%s'}," % (product.id, product.title, product.get_product_price(), item['quantity'], item['total_price'], product.get_thumbnail(), url, product.num_available)

        productsstring = productsstring + b

    if request.user.is_authenticated:
        first_name = request.user.first_name
        last_name = request.user.last_name
        email = request.user.email
        address = request.user.userprofile.address
        phone = request.user.userprofile.phone
    else:
        first_name = last_name = email = address = phone = ''

    context = {
        'cart': cart,
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'address': address,
        'phone': phone,
        
        'productsstring': productsstring.rstrip(',')
    }

    return render(request, 'cart/cart.html', context)

def success(request):
    cart = Cart(request)
    cart.clear()
    
    return render(request, 'cart/success.html')