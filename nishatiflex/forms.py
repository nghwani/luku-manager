from django import forms
from .models import MeterInfo, EnergyPurchased
    
class MeterInfoForm(forms.ModelForm):
    class Meta:
        model = MeterInfo
        fields = ['meter_number', 'location']
        widgets = {
            'meter_number': forms.TextInput(attrs={'class':'form-control'}),
            'location': forms.TextInput(attrs={'class':'form-control'})
        }



class EnergyPurchaseForm(forms.ModelForm):

    EXPECTED_DAYS_CHOICE = [
        (7,"1 Week"),
        (14,"2 Weeks"),
        (30,"1 Month"),
        (60,"2 Months")
    ]

    expected_days = forms.ChoiceField(choices=EXPECTED_DAYS_CHOICE, label="How long would it last?", widget=forms.Select(attrs={'class':'form-control'}))

    class Meta:
        model = EnergyPurchased
        fields = ['amount', 'purchase_date','expected_days', 'notes']
        widgets ={
            'amount': forms.NumberInput(attrs={'class':'form-control', 'id':'amountInput'}),
            'purchase_date': forms.DateInput(attrs={'class':'form-control', 'id':'dateInput', 'type':'date'}),
            'notes': forms.Textarea(attrs={'class':'form-control', 'rows':3})
        }

        
class FilterDateForm(forms.Form):
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class':'form', 'id':'startDateInput', 'type':'date'}),
        label='Start Date'
    )

    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class':'form', 'id':'endDateInput', 'type':'date'}),
        label='End Date'
    )


