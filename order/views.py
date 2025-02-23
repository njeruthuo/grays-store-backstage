
from .models import Order

from order.serializers import OrderSerializer
from users.authentication import Authenticator, TokenAuthentication

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response


class OrderAPIView(APIView):
    authentication_classes = [TokenAuthentication, Authenticator]

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(
            user=request.user, transaction__receipt_number__regex=r".+")

        serializer_data = OrderSerializer(orders, many=True).data
        return Response(serializer_data, status=status.HTTP_200_OK)


order_api_view = OrderAPIView.as_view()
