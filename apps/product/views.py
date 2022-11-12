import random

from django.contrib import messages
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect

from apps.vendor.models import Vendor

from .forms import AddToCartForm
from .models import Category, Product, ProductReview

from apps.cart.cart import Cart

def search(request):
    query = request.GET.get('query', '')
    products = Product.objects.filter(Q(title__icontains=query) | Q(description__icontains=query))
    category = Category.objects.filter(Q(title__icontains=query))
    vendor = Vendor.objects.filter(Q(business_name__icontains=query))
    
    
    return render(request, 'product/search.html', {
        'products': products, 
        'category':category,
        'vendor':vendor,
        'query': query, 
        })

def product(request, category_slug, product_slug):

    product = get_object_or_404(Product, category__slug=category_slug, slug=product_slug)
    product.num_visits = product.num_visits + 1

    imagesstring = '{"thumbnail": "%s", "image": "%s", "id": "mainimage"},' % (product.get_thumbnail(), product.image.url)

    for image in product.images.all():
        imagesstring += ('{"thumbnail": "%s", "image": "%s", "id": "%s"},' % (image.get_thumbnail(), product.image.url, image.id))
    
    # Add review

    if request.method == 'POST' and request.user.is_authenticated:
        stars = request.POST.get('stars', 3)
        content = request.POST.get('content', '')

        review = ProductReview.objects.create(product=product, user=request.user, stars=stars, content=content)

        return redirect('product_detail', category_slug=category_slug, slug=product_slug)

    
    similar_products = list(product.category.products.exclude(id=product.id))

    if len(similar_products) >= 4:
        similar_products = random.sample(similar_products, 4)
    
    cart = Cart(request)
    if cart.has_product(product.id):
        product.in_cart = True
    else:
        product.in_cart = False


    context = {
        
        'product': product,
        'similar_products': similar_products,
        'imagesstring': "[" + imagesstring.rstrip(',') + "]"
    }

    return render(request, 'product/product.html', context)

def category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)

    return render(request, 'product/category.html', {'category': category})