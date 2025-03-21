from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('verify_email/<str:token>', views.verify_email, name='verify_email'),
    path('verify_phone/', views.verify_phone, name='verify_phone'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout')
]

