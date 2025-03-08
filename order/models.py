from django.db import models
from django.contrib.auth import get_user_model

from catalogue.models import Product
from mpesa.models import MpesaTransaction

User = get_user_model()


class Order(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="orders")
    date_created = models.DateTimeField(auto_now_add=True)
    transaction = models.ForeignKey(
        MpesaTransaction, on_delete=models.CASCADE, related_name='order')
    delivered = models.BooleanField(default=False)
    payment_completed = models.BooleanField(default=True)
    lipa_mdogo = models.BooleanField(default=False)
    outstanding_balance = models.DecimalField(
        decimal_places=2, max_digits=12, default=0.0)

    def __str__(self):
        return f"Order {self.transaction.receipt_number} by {self.transaction.phone_number}"


class OrderPayment(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='payments')
    transaction = models.ForeignKey(MpesaTransaction, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)
    date_paid = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction.receipt_number} - {self.amount_paid}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
