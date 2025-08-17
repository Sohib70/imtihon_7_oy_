from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token
from rest_framework.status import HTTP_400_BAD_REQUEST
from django.contrib.auth import authenticate
from .models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=15, write_only=True)
    confirm_password = serializers.CharField(max_length=15, write_only=True)

    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','username','age','adres','password','confirm_password']

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise ValidationError({'message':'Parollar mos emas!','status':HTTP_400_BAD_REQUEST})
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create(
            username = validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            age=validated_data['age'],
            adres=validated_data['adres'],
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user


class LoginSerializers(serializers.Serializer):
    username = serializers.CharField(max_length=120)
    password = serializers.CharField(max_length=100, write_only=True)

    def validate(self, data):
        if not data['username'] or not data['password']:
            raise ValidationError({'error':"Login yoki parol no'togri","status":HTTP_400_BAD_REQUEST})
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise ValidationError({'error':"Login yoki parol no'togri", 'status':HTTP_400_BAD_REQUEST})
        token, _ = Token.objects.get_or_create(user=user)
        data['token'] = token.key
        return data

class ProfilSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ["id", "username", "email", "first_name", "last_name", "age", "adres"]
        read_only_fields = ['first_name']