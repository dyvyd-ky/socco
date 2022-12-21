import json
from apps.mpesa.core import MpesaClient

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
#from django.template.loader import render_to_string
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK


from apps.cart.cart import Cart
#from apps.order.views import render_to_pdf

from apps.order.utilities import checkout, notify_customer, notify_vendor

from .models import Product
from apps.order.models import Order, OrderItem


from .utilities import decrement_product_quantity, send_order_confirmation


def create_checkout_session(request):
    data = json.loads(request.body)
    #data = request.body
    cart = Cart(request)

    
    gateway = data['gateway']
    order_id = ''
    payment_intent = ''
    response = ''
    
    
    # Create order

    orderid = checkout(request, data['first_name'], data['last_name'], data['email'], data['address'], data['phone'])

    
    for item in cart:
        product = item['product']

        total_price = int(cart.get_total_cost())
        

        order = Order.objects.get(pk=orderid)
        order.paid_amount = total_price     

        
    if gateway == 'mpesa':
        cl = MpesaClient()
        phone_number = data['phone']
        
        amount = total_price
        account_reference = 'sokonisoko.com'
        transaction_desc = 'pay goods online'
        callback_url = 'https://sokonisoko.com/payments/callback/'
        
        response = cl.stk_push(phone_number, amount, account_reference, transaction_desc, callback_url)
        
        order.paid = True
        order.save()

        decrement_product_quantity(order)
        send_order_confirmation(order)
            
    else:
        order.paid = False
        order.save()
    return JsonResponse({'response':response}) 



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

