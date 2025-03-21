from django.shortcuts import render
from .models import Notification
from nishatiflex.models import EnergyPurchased
from django.contrib.auth.decorators import login_required



# Create your views here.

@login_required
def create_notification(request):
    energy_purchased = EnergyPurchased.objects.filter(user=request.user).first()

    if energy_purchased:

        if energy_purchased.expected_days > 0:
            energy_purchased.expected_days -= 1
            energy_purchased.save()

            energy_purchased.refresh_from_db()
            notification_days = energy_purchased.expected_days
            purchase_date = energy_purchased.purchase_date

            if notification_days <= 2:
                message = f"""Hi {request.user.username}! \n Your Expected days from your last purchase date {purchase_date} are below {notification_days}. 
                Make sure you top up your luku meter. Buy using the system for easy remainder and tracking."""

                Notification.objects.create(user = request.user, message = message, type='remainder')
            

@login_required
def show_notification(request):
    notifications = Notification.objects.filter(user=request.user).order_by("-created_at")
    return render(request, 'notification/show_notification.html', {'notifications': notifications})

