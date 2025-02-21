from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from .utils import get_access_token, generate_password
import requests
import json
import os
from .models import MpesaTransaction

from datetime import datetime


@api_view(['POST'])
def stk_push(request):
    access_token = get_access_token()
    password = generate_password()
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')

    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    data = request.data

    print(data, 'request data')

    print(os.getenv('MPESA_SHORTCODE'), 'shortcode')
    print("https://truly-evident-hedgehog.ngrok-free.app/callback/", 'callback url')

    payload = {
        "BusinessShortCode": os.getenv('MPESA_SHORTCODE'),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": data.get('totals'),
        "PartyA": data.get('phone'),
        "PartyB": os.getenv('MPESA_SHORTCODE'),
        "PhoneNumber": data.get('phone'),
        "CallBackURL": "https://truly-evident-hedgehog.ngrok-free.app/callback/",
        "AccountReference": "Django MPESA",
        "TransactionDesc": "Payment for services"
    }

    response = requests.post(
        'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
        headers=headers,
        json=payload
    )

    response_data = response.json()

    cartItems = data.get('cartItems')

    # Save transaction
    transaction = MpesaTransaction.objects.create(
        phone_number=request.data.get('phone_number'),
        amount=request.data.get('amount'),
        merchant_request_id=response_data.get('MerchantRequestID'),
        checkout_request_id=response_data.get('CheckoutRequestID')
    )

    print(transaction)

    return JsonResponse(response_data)


@csrf_exempt
def mpesa_callback(request):
    data = json.loads(request.body) or json.loads(request.data)

    print('callback called...')

    print('response body', data)

    # Extract callback metadata
    callback_data = data.get('Body', {}).get('stkCallback', {})

    transaction = MpesaTransaction.objects.get(
        checkout_request_id=callback_data.get('CheckoutRequestID')
    )

    transaction.result_code = callback_data.get('ResultCode')
    transaction.result_description = callback_data.get('ResultDesc')

    if callback_data.get('ResultCode') == 0:
        metadata = callback_data.get('CallbackMetadata', {}).get('Item', [])
        for item in metadata:
            if item.get('Name') == 'MpesaReceiptNumber':
                transaction.receipt_number = item.get('Value')
            elif item.get('Name') == 'Amount':
                transaction.amount = item.get('Value')
            elif item.get('Name') == 'TransactionDate':
                transaction.transaction_date = item.get('Value')
            elif item.get('Name') == 'PhoneNumber':
                transaction.phone_number = item.get('Value')

    transaction.save()

    return JsonResponse({'status': 'success'})
