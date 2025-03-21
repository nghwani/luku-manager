from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views
urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('add_meter/', views.add_meter, name='add_meter'),
    path('energy_purchased/', views.energy_purchased, name='energy_purchased'),
    path('user_profile/', views.profile_view, name='user_profile'),
    path('energy_table/', views.energy_table, name='energy_table'),
    path('purchase_data/', views.purchase_data, name='purchase_data'),
    path('purchase_data_filter/', views.purchase_data_filter, name='purchase_data_filter'),
    path('view_analytics/', views.view_analytics, name='view_analytics'),
]





