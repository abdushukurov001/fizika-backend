from django.shortcuts import render
import random
import uuid
import logging
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.hashers import make_password
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import check_password
from .serializers import CustomTokenObtainPairSerializer, OTP
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import OTP, PasswordResetToken


@api_view(['POST'])
def register_view(request):
    data = request.data
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({"error": "Bu username allaqachon mavjud!"}, status=400)

    if not username or not email or not password:
        return Response({"error": "Barcha maydonlarni to'ldirish shart!"}, status=400)

    if User.objects.filter(email=email).exists():
        return Response({"error": "Bu email allaqachon mavjud!"}, status=400)

    user_obj = User.objects.create(username=username, password=make_password(password), email=email)
    user_obj.save()

    return Response(data={'message': 'User successfuly created'}, status=201)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def change_password(request):
    user = request.user
    data = request.data

    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return Response({"error": "Both old and new passwords are required."}, status=400)

    if not check_password(old_password, user.password):
        return Response({"error": "Old password is incorrect."}, status=400)

    user.set_password(new_password)
    user.save()

    return Response({"success": "Password updated successfully."}, status=200)


@api_view(['POST'])
def forgot_password(request):
    data = request.data
    email = data.get('email')

    if not email:
        return Response({"error": "email is required"}, status=400)

    user = User.objects.filter(email=email, is_active=True).first()

    if not user:
        return Response({"error": "User not found or not verified"}, status=404)

    recent_otp = OTP.objects.filter(user=user, created_at__gte=now() - timedelta(minutes=5)).first()

    if recent_otp:
        return Response({'errro': "You can request OTP after 5 minutes"}, status=429)

    otp_code_new = random.randint(10000, 99999)
    otp_key_new = str(uuid.uuid4())
    otp = OTP.objects.create(user=user, otp_code=otp_code_new, otp_key=otp_key_new)
    otp.save()

    send_otp_email(email, otp_code_new)

    return Response({"message": "OTP code has been sent to your email", "otp_key": otp.otp_key}, status=200)


logger = logging.getLogger(__name__)


def send_otp_email(receiver_email, otp_code):
    subject = "Password Reset OTP Code"
    message = f"Your OTP code is: {otp_code}\nThis code is valid for 5 minutes."

    try:
        send_mail(
            subject,
            message,
            "abdumannofabdushukurov@gmail.com",
            [receiver_email],
            fail_silently=False,
        )
        logger.info(f"OTP email sent to {receiver_email}")
    except Exception as e:
        logger.error(f"Failed to send email to {receiver_email}: {str(e)}")


@api_view(['POST'])
def verify_otp(request):
    data = request.data
    otp_code = data.get('otp_code')
    otp_key = data.get('otp_key')

    if not otp_code or not otp_key:
        return Response({"error": " otp_code and otp_key are required"}, status=400)

    otp = OTP.objects.filter(otp_code=otp_code, otp_key__exact=otp_key,
                             created_at__gte=now() - timedelta(minutes=5)).first()

    if not otp:
        return Response({"error": "Invalid or expired OTP code ot otp_key"}, status=400)

    PasswordResetToken.objects.create(user=otp.user, otp_key=otp.otp_key)

    return Response({"otp_key": otp.otp_key}, status=200)


@api_view(['POST'])
def reset_password(request):
    data = request.data
    otp_key = data.get('otp_key')
    new_password = data.get('new_password')

    if not otp_key or not new_password:
        return Response({"error": "otp_key and new_password are required"}, status=400)

    token = PasswordResetToken.objects.filter(otp_key=otp_key).first()

    if not token:
        return Response({"error": "Invalid otp_key"}, status=400)

    user = token.user
    user.password = make_password(new_password)
    user.save()

    # token.delete()

    return Response({"message": "Password changed successfully"}, status=200)


@api_view(['GET'])
def auth_me(request):
    if not request.user.is_authenticated:
        return Response(data={"error": "auth required"}, status=401)

    return Response(data={'username': request.user.username, 'id': request.user.id})
