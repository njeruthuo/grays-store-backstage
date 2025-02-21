from django.shortcuts import render
from django.db.transaction import atomic
from .models import Order, OrderItem, Product, User


@atomic
def create_order(transaction, cartItems):
    pass


@atomic
def confirm_order_payment():
    pass
