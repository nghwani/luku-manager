from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import MeterInfo,UserProfile,EnergyPurchased
from django.db.models import Avg,Sum, Count
from .forms import MeterInfoForm, EnergyPurchaseForm, FilterDateForm
from datetime import timedelta, datetime
from django.utils import timezone
from collections import defaultdict
from django.http import JsonResponse

@login_required
def dashboard(request):
    recent_purchase = EnergyPurchased.objects.filter(user=request.user).order_by('-purchase_date')
    meter_info = MeterInfo.objects.filter(user=request.user).first()

    avg_days = recent_purchase.aggregate(Avg('expected_days'))['expected_days__avg'] or 0
    avg_amount = recent_purchase.aggregate(Avg('amount'))['amount__avg'] or 0
    total_purchase = recent_purchase.count()
    total_units = recent_purchase.aggregate(Sum('units'))['units__sum'] or 0
    
    context = {
        'recent_purchase':recent_purchase,
        'meter_info':meter_info,
        'total_purchase' :total_purchase,
        'total_units':total_units,
        'avg_days' :round(avg_days,1),
        'avg_amount' : round(avg_amount,2)
    }
    return render(request, 'luku/dashboard.html', context)

@login_required
def add_meter(request):
    if request.method == 'POST':
        form = MeterInfoForm(request.POST)
        
        if form.is_valid():
            meter_number = form.cleaned_data['meter_number']
            location = form.cleaned_data['location']
            MeterInfo.objects.update_or_create(user=request.user, defaults={'meter_number':meter_number, 'location':location})
            messages.success(request, 'Meter Info Added/Updated Successfully!')
            return redirect('dashboard')
    else:
        meter_info = MeterInfo.objects.filter(user=request.user).first()
        form = MeterInfoForm(instance=meter_info)
    return render(request, 'luku/add_meter.html', {'form':form})

@login_required
def energy_purchased(request):
    if request.method == 'POST':
        form = EnergyPurchaseForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            expected_days = form.cleaned_data['expected_days']
            purchase_date = form.cleaned_data['purchase_date']
            notes = form.cleaned_data['notes']

            purchase = EnergyPurchased.objects.create(
                user=request.user, 
                amount=amount, 
                expected_days=expected_days,
                purchase_date=purchase_date,
                notes=notes
                )
            
            user_profile = UserProfile.objects.filter(user=request.user).first()
            if user_profile:
                try:
                    units = user_profile.get_energy_purchased()
                    daily_consumption = user_profile.get_daily_consumption()
                    remaining_days = user_profile.get_remaining_days()
                    remaining_energy = user_profile.get_remaining_energy()

                    purchase.units = units
                    purchase.daily_consumption = daily_consumption
                    purchase.remaining_days = remaining_days
                    purchase.remaining_energy = remaining_energy
                    purchase.save()
                except Exception as e:
                    messages.warning(request, f'something went wrong {str(e)}')
                    purchase.delete()
                    return redirect('dashboard')       
            else:
                messages.warning(request, 'User profile not found, please contact customer support.')
                purchase.delete()
                return redirect('dashboard')
            
            messages.success(request,'successful recorded!')
            return redirect('dashboard')
    else:
        form = EnergyPurchaseForm()
    return render(request, 'luku/energy_purchased.html', {'form':form})

@login_required
def energy_table(request):
    recent_purchase = EnergyPurchased.objects.filter(user=request.user).order_by('-purchase_date')
    context = {
        'recent_purchase': recent_purchase
    }
    return render(request, 'luku/energy_table.html', context)


@login_required
def profile_view(request):
    user_profile = UserProfile.objects.filter(user=request.user).first()
    if not user_profile:
        messages.error(request, 'UserProfile not found, please contact support')
        return redirect('dashboard')
    return render(request, 'luku/user_profile.html', {'user_profile':user_profile})

@login_required
def purchase_data(request):
    # This returns a Json response with data by a month ago

    todays_date = timezone.now()
    month_ago = todays_date - timedelta(days=30)


    purchase = EnergyPurchased.objects.filter(user=request.user, 
                                              purchase_date__gte=month_ago, 
                                              purchase_date__lte=todays_date
                                              )
    finalrep = defaultdict(lambda:{'amount':0, 'units':0})

    for item in purchase:
        if item.purchase_date:
            try:
                aware_date = timezone.localtime(item.purchase_date)
                date = aware_date.strftime("%b %d, %Y")
                finalrep[date]["amount"] += item.amount
                finalrep[date]["units"] += item.units
            except ValueError as e:
                messages.error(request, f"Error formating date:{item.purchase_date} - {e}")
                continue


    dates = sorted(finalrep.keys(), key=lambda x: timezone.datetime.strptime(x, "%b %d, %Y"))
    amounts = [finalrep[date]["amount"] for date in dates]
    units = [finalrep[date]["units"] for date in dates]

    return JsonResponse({"date": dates, "amount": amounts, "units": units})


@login_required
def purchase_data_filter(request):
        # This filters for specific choosen days
        queryset = EnergyPurchased.objects.filter(user=request.user)
        
    
        if request.method == 'POST':
            form = FilterDateForm(request.POST)

            if form.is_valid():
                start_date = form.cleaned_data['start_date']
                end_date = form.cleaned_data['end_date']

                if start_date:
                    start_date = timezone.make_aware(datetime.combine(start_date, datetime.min.time()))
                    queryset = queryset.filter(purchase_date__gte=start_date)
                if end_date:
                    end_date = timezone.make_aware(datetime.combine(end_date, datetime.max.time()))
                    queryset = queryset.filter(purchase_date__lte=end_date)
                
                finalrep = defaultdict(lambda:{'amount':0, 'units':0})

                for item in queryset:
                    aware_date = timezone.localtime(item.purchase_date)
                    date = aware_date.strftime("%b %d, %Y")
                    finalrep[date]['amount'] += item.amount
                    finalrep[date]['units'] += item.units

                dates = sorted(finalrep.keys(), key=lambda x: timezone.datetime.strptime(x, "%b %d, %Y"))
                
                data = {
                    'date': dates,
                    'amount': [finalrep[date]['amount'] for date in dates],
                    'units': [finalrep[date]['units'] for date in dates]
                }

                return JsonResponse(data)
        return JsonResponse({"error":"Invalid form submission"}, status=400)

@login_required
def view_analytics(request):
    form = FilterDateForm()
    return render(request, 'luku/view_analytics.html', {"form":form})



