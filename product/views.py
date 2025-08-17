from django.shortcuts import render
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import AvtotovarlarSerializer
from .models import Avtotovarlar
from rest_framework import status
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from users.user_perm import IsUser
from rest_framework.permissions import IsAuthenticated
# Create your views here.

class AvtotovarListCreate(APIView):

    def get(self,request):
        avtotovarlar = Avtotovarlar.objects.all()
        category = request.GET.get('category')
        name = request.GET.get('name')
        price = request.GET.get('price')
        price_gt = request.GET.get('price_gt')
        price_lt = request.GET.get('price_lt')
        search = request.GET.get('search')
        ordering = request.GET.get('ordering')
        if category:
            avtotovarlar = avtotovarlar.filter(category=category)
        if name:
            avtotovarlar = avtotovarlar.filter(name__icontains=name)
        if price:
            avtotovarlar = avtotovarlar.filter(price=price)
        if price_gt:
            avtotovarlar = avtotovarlar.filter(price__gt=price_gt)
        if price_lt:
            avtotovarlar = avtotovarlar.filter(price__lt=price_lt)
        if search:
            avtotovarlar = avtotovarlar.filter(Q(name__icontains = search) | Q(price__icontains = search))
        if ordering:
            avtotovarlar = avtotovarlar.order_by(ordering)
        paginator = PageNumberPagination()
        paginator.page_size = 3
        result_page = paginator.paginate_queryset(avtotovarlar,request)
        serializers = AvtotovarlarSerializer(result_page , many=True)
        return paginator.get_paginated_response(serializers.data)

    @swagger_auto_schema(request_body=AvtotovarlarSerializer)
    def post(self,request):
        serializer = AvtotovarlarSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Muvaffaqqaiyatli qushildi",'status':status.HTTP_201_CREATED})

class AvtotovarDetailUpdateDelete(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self,request,pk):
        avtotovar = Avtotovarlar.objects.get(id = pk)
        serializer = AvtotovarlarSerializer(avtotovar)
        return Response({'data':serializer.data,'status':status.HTTP_200_OK})

    @swagger_auto_schema(request_body=AvtotovarlarSerializer)
    def put(self,request,pk):
        avtotovar = Avtotovarlar.objects.get(id=pk)
        self.check_object_permissions(request, avtotovar)
        serializer = AvtotovarlarSerializer(avtotovar,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'xabar':'uzgartirildi','data':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def patch(self,request,pk):
        avtotovar = Avtotovarlar.objects.get(id=pk)
        self.check_object_permissions(request, avtotovar)
        serializer = AvtotovarlarSerializer(avtotovar,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'xabar':'uzgartirildi','data':serializer.data},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        avtotovar = Avtotovarlar.objects.get(id=pk)
        self.check_object_permissions(request, avtotovar)
        avtotovar.delete()
        return Response({'xabar':'uchirildi'},status=status.HTTP_200_OK)