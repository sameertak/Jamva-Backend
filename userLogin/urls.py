from django.contrib import admin
from django.urls import path, include
from .views import OtpLogin, userVerify

urlpatterns = [
    path("<phone>/<name>", OtpLogin.as_view()),
    path("verify/", userVerify.as_view())
]
