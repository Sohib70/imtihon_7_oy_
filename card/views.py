from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from users.user_perm import IsUser
from product.models import Avtotovarlar
from .serializers import CardItemSerializer, CardSerializer
from .models import Card, CardItem
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


class CardCreate(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CardSerializer)
    def post(self, request):
        card, created = Card.objects.get_or_create(user=request.user)
        serializer = CardSerializer(card)
        return Response(
            data=serializer.data,
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class AddToCard(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CardSerializer)
    def post(self, request):
        product_id = request.data.get("product_id")
        amount = request.data.get("amount")

        if not product_id or not amount:
            return Response(
                {"error": "product_id va amount kerak"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            amount = int(amount)
        except ValueError:
            return Response(
                {"error": "amount butun son bo‘lishi kerak"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if amount <= 0:
            return Response(
                {"error": "Miqdor 0 yoki manfiy bo‘lishi mumkin emas"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product = Avtotovarlar.objects.filter(id=product_id).first()
        if not product:
            return Response(
                {"error": "Siz mavjud bo‘lmagan tovar tanladingiz"},
                status=status.HTTP_404_NOT_FOUND
            )

        card, _ = Card.objects.get_or_create(user=request.user)
        item, created = CardItem.objects.get_or_create(card=card, product=product)
        if created:
            item.amount = amount
        else:
            item.amount += amount
        item.save()

        serializer = CardItemSerializer(item)
        return Response(
            {
                "data": serializer.data,
                "msg": "Mahsulot savatga qo‘shildi" if created else "Mahsulot soni yangilandi"
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )


class CardItemUpdate(APIView):
    permission_classes = [IsUser]

    @swagger_auto_schema(request_body=CardItemSerializer)
    def patch(self, request, pk):
        count = request.data.get('count')
        mtd = request.data.get('mtd')

        product = get_object_or_404(CardItem, card__user=request.user, id=pk)

        if count is not None:
            try:
                product.amount = int(count)
                if product.amount <= 0:
                    product.delete()
                    return Response(
                        {"msg": "Mahsulot savatdan olib tashlandi"},
                        status=status.HTTP_204_NO_CONTENT
                    )
                product.save()
            except ValueError:
                return Response(
                    {"error": "count butun son bo‘lishi kerak"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        elif mtd:
            if mtd == "+":
                product.amount += 1
                product.save()
            elif mtd == "-":
                if product.amount == 1:
                    product.delete()
                    return Response(
                        {"msg": "Mahsulot savatdan olib tashlandi"},
                        status=status.HTTP_204_NO_CONTENT
                    )
                else:
                    product.amount -= 1
                    product.save()
            else:
                return Response(
                    {"error": "mtd faqat '+' yoki '-' bo‘lishi mumkin"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"error": "count yoki mtd berilishi kerak"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CardItemSerializer(product)
        return Response(
            {'data': serializer.data, 'status': status.HTTP_200_OK, 'msg': "O'zgartirildi"}
        )


class RemoveFromCard(APIView):
    permission_classes = [IsUser]

    def delete(self, request, pk):
        item = get_object_or_404(CardItem, card__user=request.user, id=pk)
        item.delete()
        return Response({"msg": "Mahsulot savatdan o‘chirildi"},
                        status=status.HTTP_204_NO_CONTENT)


class ClearCard(APIView):
    permission_classes = [IsUser]

    @swagger_auto_schema(request_body=CardItemSerializer)
    def delete(self, request):
        card, _ = Card.objects.get_or_create(user=request.user)
        card.items.all().delete()
        return Response({"msg": "Savat tozalandi"},
                        status=status.HTTP_204_NO_CONTENT)
