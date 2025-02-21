from django.contrib import admin

from .models import MpesaTransaction


@admin.register(MpesaTransaction)
class MpesaTransactionAdmin(admin.ModelAdmin):
    search_fields = ['receipt_number',
                     'merchant_request_id', 'checkout_request_id']
    list_display = ['phone_number', 'receipt_number', 'transaction_date']
    ordering = ['transaction_date', 'created_at']
