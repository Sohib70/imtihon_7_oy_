from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'product', 'text', 'created_at', 'updated_at']
        read_only_fields = ['user', 'product', 'created_at','updated_at']
