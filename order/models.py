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

    def __str__(self):
        return f"Order {self.id} by {self.user}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order {self.order.id}"
