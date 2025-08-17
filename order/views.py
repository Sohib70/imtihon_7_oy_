from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authentication import TokenAuthentication
from .models import Order, OrderItem
from .serializers import OrderSerializer
from card.models import Card, CardItem
from drf_yasg.utils import swagger_auto_schema


class OrderCreate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=OrderSerializer)
    def post(self, request):
        card = get_object_or_404(Card, user=request.user)
        if not card.items.exists():
            return Response({"error": "Savat bo‘sh"}, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(user=request.user)
        for item in card.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                amount=item.amount
            )
        card.items.all().delete()

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderList(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.filter(user=request.user)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)


class OrderDetail(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderStatusUpdate(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    @swagger_auto_schema(request_body=OrderSerializer)
    def patch(self, request, pk):
        order = get_object_or_404(Order, id=pk)
        status_value = request.data.get('status')
        if status_value not in ['pending', 'paid', 'shipped', 'canceled']:
            return Response({"error": "Status noto‘g‘ri"}, status=status.HTTP_400_BAD_REQUEST)
        order.status = status_value
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderCancel(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=OrderSerializer)
    def delete(self, request, pk):
        order = get_object_or_404(Order, id=pk, user=request.user)
        if order.status != 'pending':
            return Response({"error": "Faqat pending buyurtmani bekor qilish mumkin"},
                            status=status.HTTP_400_BAD_REQUEST)
        order.status = 'canceled'
        order.save()
        return Response({"msg": "Buyurtma bekor qilindi"}, status=status.HTTP_204_NO_CONTENT)
