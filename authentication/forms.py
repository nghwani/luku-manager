from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from nishatiflex.models import MeterInfo
import re

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ['first_name','last_name','username', 'email', 'phone_number', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].widget.attrs['placeholder'] = self.fields[field].label

    def clean_phone_number(self):
        phone = self.cleaned_data.get('phone_number')
        # Basic Tanzanian phone number validation
        pattern = r'^\+255\d{9}$|^0\d{9}$'
        if not re.match(pattern, phone):
            raise forms.ValidationError(
                'Enter a valid Tanzanian phone number (e.g., +255123456789 or 0123456789)'
            )
        return phone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered')
        return email
    
    
    def save(self, commit = True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']

        if commit:
            user.save()

            MeterInfo.objects.create(
                user=user,
                meter_number = self.cleaned_data['meter_number'],
                phone_number = self.cleaned_data['phone_number'],
                location = self.cleaned_data['location']
            )

        return user

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, 
                               widget=forms.TextInput(attrs={
                                   'class': 'form-control',
                                   'placeholder': 'Enter Username'
                               }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password'
    }))


