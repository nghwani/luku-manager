from django.contrib import admin
from .models import MeterInfo, EnergyPurchased, UserProfile
# Register your models here.


admin.site.register(MeterInfo)
admin.site.register(EnergyPurchased)
admin.site.register(UserProfile)



