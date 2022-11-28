from django.db import models
from django.contrib.auth.models import User
from apps.users.models import Userprofile

from apps.product.models import Product
from apps.vendor.models import Vendor

class Order(models.Model):
    ORDERED = 'ordered'
    SHIPPED = 'shipped'
    ARRIVED = 'arrived'

    STATUS_CHOICES = (
        (ORDERED, 'Ordered'),
        (SHIPPED, 'Shipped'),
        (ARRIVED, 'Arrived')
    )

    user = models.ForeignKey(User, related_name='orders', on_delete=models.SET_NULL, blank=True, null=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)

    created_at = models.DateTimeField(auto_now_add=True)

    paid = models.BooleanField(default=False)
    paid_amount = models.FloatField(blank=True, null=True)
    vendors = models.ManyToManyField(Vendor, related_name='orders')
    

    payment_intent = models.CharField(max_length=255)

    shipped_date = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ORDERED)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return '%s' % self.first_name
    
    def get_total_quantity(self):
        return sum(int(item.quantity) for item in self.items.all())
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.DO_NOTHING)
    price = models.FloatField()
    discount = models.FloatField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    vendor = models.ForeignKey(Vendor, related_name='items', on_delete=models.CASCADE)
    vendor_paid = models.BooleanField(default=False)

    def __str__(self):
        return "{}, {}".format(self.vendor, self.id)
    
    def get_total_price(self):
        return self.price * self.quantity
    
    def get_total_discount_item_price(self):
        return self.quantity * self.discount

    def get_amount_saved(self):
        return self.get_total_price() - self.get_total_discount_item_price()

    def get_final_price(self):
        if self.discount:
            return self.get_total_discount_item_price()
        return self.get_total_price()


    