from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
import os
import json
import requests
from datetime import datetime

from django.http import JsonResponse
from django.db.transaction import atomic
from django.views.decorators.csrf import csrf_exempt

from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated

from payment.consumers import MPESAConsumer

from .models import MpesaTransaction
from order.models import Order, OrderItem, Product
from users.authentication import Authenticator, TokenAuthentication
from .utils import get_access_token, generate_password, time_format_helper


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

    payload = {
        "BusinessShortCode": os.getenv('MPESA_SHORTCODE'),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": data.get('totals'),
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

    response_data = response.json()

    cartItems = data.get('cartItems')

    transaction = MpesaTransaction.objects.create(
        phone_number=request.data.get('phone'),
        amount=request.data.get('totals'),
        merchant_request_id=response_data.get('MerchantRequestID'),
        checkout_request_id=response_data.get('CheckoutRequestID')
    )

    order = Order.objects.create(
        user=request.user,
        transaction=transaction,
    )

    for item in cartItems:

        product = Product.objects.get(id=item['product']['id'])
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=item['quantity'],
            price=item['product']['price'],
        )

    return JsonResponse(response_data)


@csrf_exempt
def mpesa_callback(request):
    consumer = MPESAConsumer()
    data = json.loads(request.body) or json.loads(request.data)

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
