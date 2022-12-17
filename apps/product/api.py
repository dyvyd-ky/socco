import json
import requests
from requests.auth import HTTPBasicAuth
import json
from .mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword

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



def getAccessToken(request):
    consumer_key = settings.MPESA_CONSUMER_KEY
    consumer_secret = settings.MPESA_CONSUMER_SECRET 
    api_URL = 'https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']
    return HttpResponse(validated_mpesa_access_token)

def pay_soko():
    data = json.loads(request.body)
    cart = Cart(request)
    orderid = checkout(request, data['first_name'], data['last_name'], data['email'], data['address'], data['phone'])

    
    for item in cart:
        product = item['product']

        total_price = int(cart.get_total_cost())
        

        order = Order.objects.get(pk=orderid)
        order.paid_amount = total_price

    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": total_price,
        "PartyA": data['phone'],  
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": data['phone'],  
        "CallBackURL": "https://sokoni.herokuapp.com/api/payments/lnm/",
        "AccountReference": "sokonisoko.com",
        "TransactionDesc": "payment of goods"
    }
    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')




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
