from email.policy import default
from django.contrib.auth.models import User
from django.db import models

class Vendor(models.Model):
    business_name = models.CharField(max_length=255)
    profile_pic = models.ImageField(default='/uploads/star.jpg')
    about = models.TextField(max_length=380)
    instagram_url = models.URLField(null=True, blank=True)
    twitter_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(User, related_name='vendor', on_delete=models.CASCADE)
    email = models.EmailField()
    
    

    class Meta:
        ordering = ['business_name']
    
    def __str__(self):
        return self.business_name
    
    def get_balance(self):
        items = self.items.filter(vendor_paid=False, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(vendor_paid=True, order__vendors__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)