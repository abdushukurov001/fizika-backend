from django.urls import path
from rest_framework_simplejwt.views import  TokenRefreshView
from .views import register_view, auth_me, CustomTokenObtainPairView, change_password, forgot_password, reset_password, verify_otp

urlpatterns = [
    path('login/',  CustomTokenObtainPairView.as_view()),
    path('register/', register_view),
    path('refresh/', TokenRefreshView.as_view()),
    path('change-password/', change_password),
    path('forgot-password/', forgot_password),
    path('verify-otp/', verify_otp),
    path('reset-password/', reset_password),
    path('auth-me/', auth_me)

]