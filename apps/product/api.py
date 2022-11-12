import json
import stripe
#import razorpay

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string

#from paypalcheckoutsdk.core import PayPalHttpClient, SandboxEnvironment
#from paypalcheckoutsdk.orders import OrdersCaptureRequest

from apps.cart.cart import Cart
#from apps.order.views import render_to_pdf

from apps.order.utilities import checkout

from .models import Product
from apps.order.models import Order
#from apps.coupon.models import Coupon

from .utilities import decrement_product_quantity, send_order_confirmation



def create_checkout_session(request):
    data = json.loads(request.body)
    cart = Cart(request)
    

    gateway = data['gateway']
    session = ''
    order_id = ''
    payment_intent = ''

    # Create order

    orderid = checkout(request, data['first_name'], data['last_name'], data['email'], data['location'], data['phone'])

    total_price = 0.00

    for item in cart:
        product = item['product']
        total_price = total_price + (float(product.price) * int(item['quantity']))

    
    
    order = Order.objects.get(pk=orderid)
    order.paid_amount = total_price
    order.save()


    return JsonResponse({'session': session, 'order': payment_intent})


def api_add_to_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = data['product_id']
    update = data['update']
    quantity = data['quantity']

    cart = Cart(request)

    product = get_object_or_404(Product, pk=product_id)

    if not update:
        cart.add(product=product, quantity=1, update_quantity=False)
    else:
        cart.add(product=product, quantity=quantity, update_quantity=True)
    
    return JsonResponse(jsonresponse)

def api_remove_from_cart(request):
    data = json.loads(request.body)
    jsonresponse = {'success': True}
    product_id = str(data['product_id'])

    cart = Cart(request)
    cart.remove(product_id)

    return JsonResponse(jsonresponse)