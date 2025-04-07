from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import OTP
from django.contrib.auth.hashers import check_password
from rest_framework.exceptions import APIException


class OtpSerializer(serializers.ModelSerializer):
    class Meta:
        model= OTP
        fields=["id", "otp_code", "otp_key"]



class NotFoundException(APIException):
    status_code = 404
    default_detail = 'Foydalanuvchi topilmadi.'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        username = attrs.get("username")
        password = attrs.get("password")

        try:
             user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise NotFoundException()  # bu yerda ishlatiladi

        if not check_password(password, user.password):
            raise serializers.ValidationError({"error": "Parol noto'g'ri!"})
        
        if not user.is_active:
            raise serializers.ValidationError({"error": "Bu foydalanuvchi aktiv emas!"})
        
        return super().validate(attrs)