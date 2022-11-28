from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils.text import slugify
from django.shortcuts import render, redirect, get_object_or_404

from apps.product.views import product
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import DeleteView
from .models import Vendor
from apps.product.models import Product, ProductImage
from apps.order.models import Order, OrderItem


from .forms import ProductForm, ProductImageForm, VendorForm

def become_vendor(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()

            return redirect('login')
    else:
        form = UserCreationForm()

    return render(request, 'vendor/become_vendor.html', {'form': form})

@login_required
def vendor_admin(request):
    try:
        vendor = request.user.vendor
        products = vendor.products.all()
        orders = vendor.orders.all()
        paid_amount=0
        balance = 0
        
        

        for order in orders:
            order.fully_paid = True
            for item in order.items.all():
                if item.vendor == request.user.vendor:
                    if item.vendor_paid == True:
                        paid_amount += item.get_final_price()
                    else:    
                        balance += item.get_final_price()
                        order.fully_paid = False

      
        return render(request, 'vendor/vendor_admin.html', {'vendor': vendor, 'products': products, 'orders': orders, 'paid_amount':paid_amount, 'balance':balance})
    except:
        pass
        return redirect('/')

    

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.vendor = request.user.vendor
            product.slug = slugify(product.title)
            product.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm()
    
    return render(request, 'vendor/add_product.html', {'form': form})

@login_required
def edit_product(request, pk):
    vendor = request.user.vendor
    product = vendor.products.get(pk=pk)

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        #image_form = ProductImageForm(request.POST, request.FILES)

        '''if image_form.is_valid():
            productimage = image_form.save(commit=False)
            productimage.product = product
            productimage.save()

            return redirect('vendor_admin')'''

        if form.is_valid():
            form.save()

            return redirect('vendor_admin')
    else:
        form = ProductForm(instance=product)
        #image_form = ProductImageForm()
    
    return render(request, 'vendor/edit_product.html', {'form': form, 'product': product})

@login_required
def edit_vendor(request):
    if request.method == 'POST':
        form = VendorForm(request.POST,
                                    request.FILES,
                                    instance=request.user.vendor)
        if form.is_valid():
            form.save()
           
            return redirect('vendor_admin')
    else:
        form = VendorForm(instance=request.user.vendor)
        

    context = {
        'form': form,
    }
    return render(request, 'vendor/edit_vendor.html', context)

def vendors(request):
    vendors = Vendor.objects.all()
    

    return render(request, 'vendor/vendors.html', {'vendors': vendors})

def vendor(request, vendor_id):
    vendor = get_object_or_404(Vendor, pk=vendor_id)

    return render(request, 'vendor/vendor.html', {'vendor': vendor})

class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = '/'
    
    def test_func(self):
        product = self.get_object()
        if self.request.user == product.vendor:
            return True
        return False

'''@login_required
def delete_product(request, pk):
    product = Product.objects.filter(user=request.user).get(pk=pk)
    #product.status = Product.DELETED
    product.save()

    #messages.success(request, 'The product was deleted!')

    return redirect('/')
'''
