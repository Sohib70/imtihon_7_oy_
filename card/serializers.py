from rest_framework import serializers
from .models import Card,CardItem


class CardItemSerializer(serializers.ModelSerializer):
    total_price = serializers.ReadOnlyField()
    card = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = CardItem
        fields = ['id','card','product','amount','created_at','update_at','total_price']


class CardSerializer(serializers.ModelSerializer):
    items = CardItemSerializer(many=True,read_only=True)
    total_price = serializers.ReadOnlyField()
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Card
        fields = ['id','user','created_at','total_price','items']
