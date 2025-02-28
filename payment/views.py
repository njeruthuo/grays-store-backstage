# from django.views.decorators.csrf import csrf_exempt
# from django.http import JsonResponse
# from rest_framework import status
# from rest_framework.response import Response
# from rest_framework.views import APIView
# import base64
# import datetime
# import json
# from asgiref.sync import async_to_sync
# from channels.layers import get_channel_layer

# import requests
# import os
# from requests.auth import HTTPBasicAuth

# from order.models import Order, OrderItem

# import logging

# logger = logging.getLogger(__name__)

# MPESA_CONSUMER_KEY = os.getenv("CONSUMER_KEY")
# MPESA_CONSUMER_SECRET = os.getenv("CONSUMER_SECRET")
# MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
# MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")
# MPESA_CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL")


# def send_payment_confirmation(transaction_id):
#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "payments",  # Group name
#         {
#             "type": "send_payment_update",
#             "data": {"message": f"Payment {transaction_id} confirmed!"}
#         }
#     )


# def get_mpesa_access_token():
#     url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
#     response = requests.get(url, auth=HTTPBasicAuth(
#         MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET
#     ))

#     if response.status_code == 200:
#         return response.json()["access_token"]
#     else:
#         raise Exception("Failed to get MPESA access token")


# def stk_push(phone_number, amount, order_id):
#     partyB = os.getenv("MPESA_SHORTCODE")
#     callBack = os.environ.get("MPESA_CALLBACK_URL")
#     shortCode = os.getenv("MPESA_SHORTCODE")

#     print(partyB, 'partyB')
#     print(callBack, 'callBack URL')
#     print(shortCode, 'shortCode')

#     access_token = get_mpesa_access_token()
#     url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

#     timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
#     password = base64.b64encode(
#         f"{os.getenv('MPESA_SHORTCODE')}{os.getenv(
#             'MPESA_PASSKEY')}{timestamp}".encode()
#     ).decode()

#     headers = {
#         "Authorization": f"Bearer {access_token}",
#         "Content-Type": "application/json"
#     }

#     payload = {
#         "BusinessShortCode": shortCode,
#         "Password": password,
#         "Timestamp": timestamp,
#         "TransactionType": "CustomerPayBillOnline",
#         "Amount": amount,
#         "PartyA": phone_number,
#         "PartyB": partyB,
#         "PhoneNumber": phone_number,
#         "CallBackURL": callBack,
#         "AccountReference": f"Order-{order_id}",
#         "TransactionDesc": "Payment for order"
#     }

#     response = requests.post(url, json=payload, headers=headers)
#     return response.json()


# def create_an_order(user, phone, amount, product_list):
#     """Call this function when initiating the order creation"""
#     order = Order.objects.create(user=user, transactionID="", delivered=False)

#     for product_obj in product_list:
#         OrderItem.objects.create(
#             order=order,
#             # Assuming product_obj is a dictionary
#             product=product_obj["product"],
#             quantity=product_obj["quantity"],
#             price=product_obj["price"],  # Store price at purchase time
#         )

#     return order





# class CallBackAPIView(APIView):
#     def post(self, request, *args, **kwargs):
#         print(args)
#         print(kwargs)
#         payload = request.data

#         print("Processing payload data....")

#         print(payload)
#         logger.info("Mpesa callback received")
#         try:
#             data = json.loads(payload)  # Parse JSON request
#             logger.info(f"Callback data received: {data}")
#             result_code = data["Body"]["stkCallback"]["ResultCode"]
#             merchant_request_id = data["Body"]["stkCallback"]["MerchantRequestID"]
#             checkout_request_id = data["Body"]["stkCallback"]["CheckoutRequestID"]

#             # If transaction was successful
#             if result_code == 0:
#                 amount = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][0]["Value"]
#                 mpesa_receipt_number = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][1]["Value"]
#                 phone_number = data["Body"]["stkCallback"]["CallbackMetadata"]["Item"][4]["Value"]

#                 # Find the order and update it
#                 order = Order.objects.filter(
#                     transactionID=checkout_request_id).first()
#                 if order:
#                     order.transactionID = mpesa_receipt_number  # Update with M-Pesa receipt
#                     order.delivered = True  # Mark as paid (or any other logic)
#                     order.save()

#                     send_payment_confirmation(mpesa_receipt_number)

#                     return Response({"message": "Payment received and order updated"}, status=200)

#             return Response({"message": "Payment failed or was canceled"}, status=400)

#         except Exception as e:
#             logger.error(f"Error processing callback: {e}")
#             return Response({"error": str(e)}, status=500)


# callback_api_view = CallBackAPIView.as_view()
