from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, timedelta
# Create your models here.
class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True)
    email_verified = models.BooleanField(default=False)
    phone_verified = models.BooleanField(default=False)

class PhoneVerification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)
    
    def is_valid(self):
        # Code expires after 10 minutes
        return datetime.now() - self.created_at.replace(tzinfo=None) <= timedelta(minutes=10)