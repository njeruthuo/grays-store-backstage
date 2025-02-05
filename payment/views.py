from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
import base64
import datetime
import json
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

import requests
import os
from requests.auth import HTTPBasicAuth

MPESA_CONSUMER_KEY = os.getenv("CONSUMER_KEY")
MPESA_CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
MPESA_CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")


def send_payment_confirmation(transaction_id):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "payments",  # Group name
        {
            "type": "send_payment_update",
            "data": {"message": f"Payment {transaction_id} confirmed!"}
        }
    )


def get_mpesa_access_token():
    url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(
        # os.getenv("MPESA_CONSUMER_KEY"),
        # os.getenv("MPESA_CONSUMER_SECRET")
        MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET
    ))

    if response.status_code == 200:
        return response.json()["access_token"]
    else:
        raise Exception("Failed to get MPESA access token")


def stk_push(phone_number, amount, order_id):
    access_token = get_mpesa_access_token()
    url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    password = base64.b64encode(
        f"{os.getenv('MPESA_SHORTCODE')}{os.getenv(
            'MPESA_PASSKEY')}{timestamp}".encode()
    ).decode()

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "BusinessShortCode": os.getenv("MPESA_SHORTCODE"),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": os.getenv("MPESA_SHORTCODE"),
        "PhoneNumber": phone_number,
        "CallBackURL": os.getenv("MPESA_CALLBACK_URL"),
        "AccountReference": f"Order-{order_id}",
        "TransactionDesc": "Payment for order"
    }

    response = requests.post(url, json=payload, headers=headers)
    return response.json()


class MPESA_APIView(APIView):
    def post(self, request, *args, **kwargs):
        return Response({}, status=status.HTTP_200_OK)


mpesa_api_view = MPESA_APIView.as_view()
