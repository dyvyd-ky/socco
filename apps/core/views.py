
from django.shortcuts import render
from apps.product.models import Product
from versone.settings import DEFAULT_EMAIL_FROM
from .forms import ContactForm

from django.conf import settings
from django.template.loader import render_to_string

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.shortcuts import render, get_object_or_404

from apps.cart.cart import Cart

def frontpage(request):
    newest_products = Product.objects.all()[0:16]
    for product in newest_products:
    
        cart = Cart(request)
        if cart.has_product(product.id):
            product.in_cart = True
        else:
            product.in_cart = False

    


    return render(request, 'core/frontpage.html', {
        'newest_products': newest_products
        })


'''def contact(request):
    form = ContactForm()
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            sender = form.cleaned_data["email"]
    

            message = Mail(
                from_email = sender,
                to_emails = settings.DEFAULT_EMAIL_FROM,
                subject= 'From Elytte Contact Form',
                html_content = render_to_string('core/contact.html', {'form': form}))
            try:
                sg = SendGridAPIClient(settings.SENDGRID_API_KEY)
                response = sg.send(message)
                print(response.status_code)
                print(response.body)
                print(response.headers)
            except Exception as e:
                print('Error!')
    return render(request, 'core/contact.html', {'form': form})'''

    
    
         
        


        
