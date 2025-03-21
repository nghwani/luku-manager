from django.contrib import admin
from .models import User, PhoneVerification
# Register your models here.

admin.site.register(User)
admin.site.register(PhoneVerification)

