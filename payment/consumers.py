from .views import stk_push
import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer


class PaymentConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "payments"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        await self.send(text_data=json.dumps({"message": "Received: " + data["message"]}))

    async def send_payment_update(self, event):
        await self.send(text_data=json.dumps(event["data"]))


class MPESAConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_name = "mpesa_payments"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        data = json.loads(text_data)
        phone_number = data["phone_number"]
        amount = data["amount"]
        order_id = data["order_id"]

        # Call the STK push function
        response = stk_push(phone_number, amount, order_id)

        # Send response to frontend
        await self.send(text_data=json.dumps(response))

    async def send_mpesa_update(self, event):
        """Sends updates to the frontend when called."""
        await self.send(text_data=json.dumps(event["data"]))
