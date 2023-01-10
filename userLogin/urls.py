from django.contrib import admin
from django.urls import path, include
from .views import OtpLogin

urlpatterns = [
    path("<phone>/<name>", OtpLogin.as_view()),
    # path("/details", userDetail.as_view())
]
