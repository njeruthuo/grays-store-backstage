from rest_framework import serializers
from .models import Order, OrderItem, Product, User, MpesaTransaction, OrderPayment


class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MpesaTransaction
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'is_superuser']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'price', 'product', 'quantity']


class OrderPaymentSerializer(serializers.ModelSerializer):
    transaction = MpesaTransactionSerializer()

    class Meta:
        model = OrderPayment
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):

    payments = OrderPaymentSerializer(many=True)
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ['id', 'date_created',
                  'delivered', 'order_items', 'payment_completed', 'lipa_mdogo', 'outstanding_balance', 'payments']

    def get_order_items(self, obj):
        items = obj.order_items.all()
        return OrderItemSerializer(items, many=True).data

    def get_payments(self, obj):
        items = obj.payments.all()
        return OrderItemSerializer(items, many=True).data
