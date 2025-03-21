from django.db import models
from django.conf import settings
from django.utils.timezone import now
from decimal import Decimal
# Create your models here.   
class MeterInfo(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, unique=True)
    meter_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    def __str__(self):
        return f'Meter: {self.meter_number}'
    

class EnergyPurchased(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    units = models.FloatField(default=0.0, null=True, blank=True)
    daily_consumption = models.FloatField(default=0.0, null=True, blank=True)
    purchase_date = models.DateTimeField(default=now)
    expected_days = models.IntegerField(default=30)
    remaining_days = models.IntegerField(default=30, null=True, blank=True)
    remaining_energy = models.FloatField(default=0.0, null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def get_energy_purchased(self):
        last_purchase = EnergyPurchased.objects.filter(user=self.user).order_by('-id').first()
        if last_purchase:
            cost_per_KWh = Decimal('357.14')
            energy_purchased = last_purchase.amount / cost_per_KWh
            return round(energy_purchased, 2)
        return Decimal(0)
    
    def get_daily_consumption(self):
        last_purchase = EnergyPurchased.objects.filter(user=self.user).order_by('-purchase_date').first()
        if last_purchase and last_purchase.expected_days > 0:
            return self.get_energy_purchased() / last_purchase.expected_days
        return 0
    
    def get_remaining_days(self):
        last_purchase = EnergyPurchased.objects.filter(user=self.user).order_by('-purchase_date').first()
        if last_purchase:
            days_used = (now() - last_purchase.purchase_date).days
            return max(last_purchase.expected_days - days_used, 0)  
        return None
    
    def get_remaining_energy(self):
        last_purchase = EnergyPurchased.objects.filter(user=self.user).order_by('-purchase_date').first()
        if last_purchase:
            remaining_days = self.get_remaining_days()
            remaining_energy = remaining_days * self.get_daily_consumption()
            return round(remaining_energy, 2)
        return Decimal(0)


