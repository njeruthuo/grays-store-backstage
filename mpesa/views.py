from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os
import json
import requests
from datetime import datetime

from django.http import JsonResponse
from django.db.transaction import atomic
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from payment.consumers import MPESAConsumer

from .models import MpesaTransaction
from order.models import Order, OrderItem, OrderPayment, Product
from users.authentication import Authenticator, TokenAuthentication
from .utils import get_access_token, generate_password, time_format_helper

from decimal import Decimal


@atomic()
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([Authenticator, TokenAuthentication])
def stk_push(request):

    if request.user.is_anonymous:
        return JsonResponse({'error': 'User not authenticated'}, status=401)

    access_token = get_access_token()
    password = generate_password()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    data = request.data

    """
    {
        order_id: items.id,
        phone,
        totals: total_sum,
        cartItems: items.order_items,
        lipaMdogo,
        mdogoAmount: Number(totals),
      }
    """

    order_to_modify = data.get("order_id")

    lipaMdogo = data.get('lipaMdogo', False)

    mdogoAmount = data.get('mdogoAmount', 0)
    totals = data.get('totals', 0)

    payload = {
        "BusinessShortCode": os.getenv('MPESA_SHORTCODE'),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": data.get('totals') if not lipaMdogo else mdogoAmount,
        "PartyA": data.get('phone'),
        "PartyB": os.getenv('MPESA_SHORTCODE'),
        "PhoneNumber": data.get('phone'),
        "CallBackURL": os.getenv('MPESA_CALLBACK_URL'),
        "AccountReference": "GRAYS ONLINE STORE",
        "TransactionDesc": "Payment for services"
    }

    response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
        headers=headers,
        json=payload
    )

    print(request.data, 'request data')

    response_data = response.json()

    cartItems = data.get('cartItems')

    transaction = MpesaTransaction.objects.create(
        phone_number=request.data.get('phone'),
        amount=totals if not lipaMdogo else mdogoAmount,
        merchant_request_id=response_data.get('MerchantRequestID'),
        checkout_request_id=response_data.get('CheckoutRequestID')
    )

    # Create Order
    outstanding_balance = totals - mdogoAmount if lipaMdogo and mdogoAmount else 0
    payment_completed = outstanding_balance == 0

    if order_to_modify:
        order = Order.objects.get(id=order_to_modify)
        order.outstanding_balance -= outstanding_balance
        order.payment_completed = payment_completed
        order.save()

    else:
        order = Order.objects.create(
            user=request.user,
            transaction=transaction,
            lipa_mdogo=lipaMdogo,
            outstanding_balance=outstanding_balance,
            payment_completed=payment_completed
        )

        # Create Order Items
        for item in cartItems:
            product = get_object_or_404(Product, id=item['product']['id'])
            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=item['quantity'],
                price=item['product']['price'],
            )

    # Log Order Payment (whether full or partial)
    OrderPayment.objects.create(
        order=order,
        transaction=transaction,
        amount_paid=mdogoAmount if lipaMdogo else totals
    )

    return JsonResponse(response_data)


@csrf_exempt
def mpesa_callback(request):
    consumer = MPESAConsumer()
    data = json.loads(request.body)

    callback_data = data.get('Body', {}).get('stkCallback', {})

    try:
        transaction = MpesaTransaction.objects.get(
            checkout_request_id=callback_data.get('CheckoutRequestID')
        )
    except MpesaTransaction.DoesNotExist:
        try:
            transaction = MpesaTransaction.objects.get(
                merchant_request_id=callback_data.get('MerchantRequestID')
            )
        except:
            print('No transaction matches this request...')

    transaction.result_code = callback_data.get('ResultCode')
    transaction.result_description = callback_data.get('ResultDesc')
    metadata = callback_data.get('CallbackMetadata', {}).get('Item', [])

    if callback_data.get('ResultCode') == 0:
        print("result code 0")
        for item in metadata:
            if item.get('Name') == 'MpesaReceiptNumber':
                transaction.receipt_number = item.get('Value')
            elif item.get('Name') == 'Amount':
                transaction.amount = item.get('Value')
            elif item.get('Name') == 'TransactionDate':
                transaction.transaction_date = time_format_helper(
                    item.get('Value'))
            elif item.get('Name') == 'PhoneNumber':
                transaction.phone_number = item.get('Value')

    elif callback_data.get('ResultCode') == 1032:
        Order.objects.get(transaction=transaction).delete()
        transaction.delete()
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "mpesa_payments",
            {
                "type": "send_mpesa_update",
                "data": metadata
            }
        )

    transaction.save()
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "mpesa_payments",
        {
            "type": "send_mpesa_update",
            "data": metadata
        }
    )

    return JsonResponse({'status': 'success'})


def send_payment_confirmation(metadata):

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "mpesa_payments",
        {
            "type": "send_mpesa_update",
            "data": metadata
        }
    )
