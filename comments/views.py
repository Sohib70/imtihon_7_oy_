from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Comment
from product.models import Avtotovarlar
from .serializers import CommentSerializer
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema

class CommentListCreate(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        product = get_object_or_404(Avtotovarlar, id=pk)
        if request.user.is_staff:
            comments = product.comments.all()
        else:
            comments = product.comments.filter(user=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, pk):
        product = get_object_or_404(Avtotovarlar, id=pk)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CommentDetailUpdateDelete(APIView):
    permission_classes = [IsAuthenticated]
    @swagger_auto_schema(request_body=CommentSerializer)
    def patch(self, request, pk):
        comment = get_object_or_404(Comment, id=pk, user=request.user)
        serializer = CommentSerializer(comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = get_object_or_404(Comment, id=pk, user=request.user)
        comment.delete()
        return Response({"msg": "Sharh o'chirildi"}, status=status.HTTP_204_NO_CONTENT)


class AllComments(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_staff:
            comments = Comment.objects.all()
        else:
            comments = Comment.objects.filter(user=request.user)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)
