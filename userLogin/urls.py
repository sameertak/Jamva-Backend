from django.contrib import admin
from django.urls import path, include
from .views import otpLogin

urlpatterns = [
    path("<phone>/<name>", otpLogin.as_view()),
]
