from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4




class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.PositiveIntegerField()
    otp_key = models.UUIDField(default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f"{self.user.username} - {self.otp_code}"
    

class PasswordResetToken(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_key = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

