from django.db import models


class MpesaTransaction(models.Model):
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number = models.CharField(max_length=50, null=True, unique=True)
    transaction_date = models.DateTimeField(null=True, auto_created=True)
    merchant_request_id = models.CharField(max_length=100, null=True)
    checkout_request_id = models.CharField(max_length=100, null=True)
    result_code = models.IntegerField(null=True)
    result_description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.phone_number} - {self.amount}"
