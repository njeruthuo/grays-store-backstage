from rest_framework import serializers
from .models import Order, OrderItem, Product, User, MpesaTransaction


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


class OrderSerializer(serializers.ModelSerializer):
    transaction = MpesaTransactionSerializer()
    order_items = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = ['id','transaction', 'date_created', 'delivered', 'order_items']

    def get_order_items(self, obj):
        items = obj.order_items.all()
        return OrderItemSerializer(items, many=True).data
