from django.contrib import admin
from django.urls import path
from .views import send_alerts

urlpatterns = [
    path('',send_alerts),
]

