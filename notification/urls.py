from django.urls import path
from . import views

urlpatterns = [
    path('show_notification/', views.show_notification, name='show_notification'),
    path('create_notification/', views.create_notification, name='create_notification')
]