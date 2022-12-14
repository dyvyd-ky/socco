import json
#from django_daraja.mpesa.core import MpesaClient
#mpesa
#mpesa
import requests
from requests.auth import HTTPBasicAuth

from .access_token import generate_access_token
from .encode import generate_password
from .timestamp import get_timestamp


from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, redirect
#from django.template.loader import render_to_string



from apps.cart.cart import Cart
#from apps.order.views import render_to_pdf

from apps.order.utilities import checkout, notify_customer, notify_vendor

from .models import Product
from apps.order.models import Order, OrderItem


from .utilities import decrement_product_quantity, send_order_confirmation



def create_checkout_session(request):
    data = json.loads(request.body)
    cart = Cart(request)

    
    gateway = data['gateway']
    session = ''
    order_id = ''
    payment_intent = ''
    
    # Create order

    orderid = checkout(request, data['first_name'], data['last_name'], data['email'], data['address'], data['phone'])

    
    for item in cart:
        product = item['product']

        total_price = int(cart.get_total_cost())
        

        order = Order.objects.get(pk=orderid)
        order.paid_amount = total_price
        
        
        

        
        if gateway == 'mpesa':
            formatted_time = get_timestamp()
            decoded_password = generate_password(formatted_time)
            access_token = generate_access_token()
            api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
            headers = {"Authorization": "Bearer %s" % access_token}
            
            
            request = {
                "BusinessShortCode": settings.MPESA_SHORTCODE,
                "Password": decoded_password,
                "Timestamp": formatted_time,
                "TransactionType": "CustomerBuyGoodsOnline",
                "Amount": total_price,
                "PartyA": data['phone'],
                "PartyB": settings.MPESA_SHORTCODE,
                "PhoneNumber": data['phone'],
                "CallBackURL": 'https://sokonisoko.com/api/payments/lnm/',
                "AccountReference": "ref",
                "TransactionDesc": "desc",
            }
            
            response = requests.post(api_url, json=request, headers=headers)
            


        if response == '0':
            order.paid = True
            order.payment_intent = order_id
            order.save()

            decrement_product_quantity(order)
            send_order_confirmation(order)
            
        else:
            order.paid = False
            order.save()
    else:
        order = Order.objects.get(pk=orderid)
        
        order.payment_intent = payment_intent
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

'''def stk_push_callback(request):
        data = request.body
        
        return HttpResponse('')'''