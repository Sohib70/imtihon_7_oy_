from rest_framework import serializers
from .models import Category,Avtotovarlar


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class AvtotovarlarSerializer(serializers.ModelSerializer):
    category = CategorySerializers(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True
    )
    class Meta:
        model = Avtotovarlar
        fields = ['id','name', 'firmasi', 'tavsifi', 'price','user', 'category', 'category_id']