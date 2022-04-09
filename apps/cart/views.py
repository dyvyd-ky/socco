import stripe 

from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect

from .cart import Cart
from .forms import CheckoutForm

from apps.order.utilities import checkout, notify_customer, notify_vendor

def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            '''
            stripe.api_key = settings.STRIPE_SECRET_KEY

            stripe_token = form.cleaned_data['stripe_token']

            try:
                charge = stripe.Charge.create(
                    amount=int(cart.get_total_cost() * 100),
                    currency='USD',
                    description='Charge from Interiorshop',
                    source=stripe_token
                )
            '''
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            location = form.cleaned_data['location']
            code = form.cleaned_data['code']
                

            order = checkout(request, first_name, last_name, email, location, phone, code, cart.get_total_cost())

            cart.clear()

            notify_customer(order)
            notify_vendor(order)

            return redirect('success')
    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'cart/cart.html', {'form': form})

def success(request):
    return render(request, 'cart/success.html')