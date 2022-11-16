from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from apps.cart.cart import Cart

from .models import Order, OrderItem

def checkout(request, first_name, last_name, email, address, phone):
    

    order = Order(first_name=first_name, last_name=last_name, email=email, address=address, phone=phone)
    if request.user.is_authenticated:
        order.user = request.user
        order.address = request.user.userprofile.address
        order.phone = request.user.userprofile.phone

        
       
    
    
        
    order.save()

    cart = Cart(request)

    for item in cart:
        OrderItem.objects.create(order=order, product=item['product'],vendor=item['product'].vendor, price=item['price'], quantity=item['quantity'])
        order.vendors.add(item['product'].vendor)
    return order.id
'''def checkout(request, first_name, last_name, email, location, phone, code, amount):
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, location=location, phone=phone, code=code, paid_amount=amount)

    for item in Cart(request):
        OrderItem.objects.create(order=order, product=item['product'], vendor=item['product'].vendor, price=item['product'].price, quantity=item['quantity'])
    
        order.vendors.add(item['product'].vendor)

    return order'''

def notify_vendor(order):

    for vendor in order.vendors.all():
        message = Mail(
            from_email = settings.DEFAULT_EMAIL_FROM,
            to_emails = vendor.created_by.email,
            subject='You have a new order!',
            html_content = render_to_string('order/email_notify_vendor.html', {'order': order, 'vendor': vendor}))
        try:
            sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print('Error! Order not successful. Please try again.')
        


def notify_customer(order):
    message = Mail(
        from_email = settings.DEFAULT_EMAIL_FROM,
        to_emails=order.email,
        subject='Thank you for the order!',
        html_content = render_to_string('order/email_notify_customer.html', {'order': order}))
    try:
        sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print('Error! Please try again.')
    
    