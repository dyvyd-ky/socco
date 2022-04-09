from django.forms import ModelForm
from django import forms
from apps.product.models import Product, ProductImage
from apps.vendor.models import Vendor

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'thumbnail', 'image', 'title','slug', 'description', 'price']

class ProductImageForm(ModelForm):
    class Meta:
        model = ProductImage
        fields = ['image']

class VendorForm(ModelForm):
    class Meta:
        model = Vendor
        fields = ['business_name', 'profile_pic', 'email', 'about', 'instagram_url', 'twitter_url', 'created_by']