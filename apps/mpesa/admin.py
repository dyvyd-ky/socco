from django.contrib import admin

# Register your models here.
from apps.mpesa.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "amount", "receipt_no", "created")

admin.site.register(Transaction,TransactionAdmin)
