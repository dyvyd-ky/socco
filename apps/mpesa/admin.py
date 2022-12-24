

# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import PaymentTransaction


# Register your models here.

class PaymentTransactionAdmin(admin.ModelAdmin):
    list_display = ("PhoneNumber", "Amount", "MpesaReceiptNumber", "TransactionDate", "ResultDesc")


admin.site.register(PaymentTransaction, PaymentTransactionAdmin)
