from django.contrib import admin
from django.urls import path, include
from .views import RestMenu, RestDetail, AvailabeCategory, AddMenu, CategoryMenu, UserOrder, FinalOrder

urlpatterns = [
    path("menu/", RestMenu.as_view()),
    path("detail/", RestDetail.as_view()),
    path("category/", AvailabeCategory.as_view()),
    path("menu/add/", AddMenu.as_view()),
    path("menu/category/", CategoryMenu.as_view()),
    path("order/", UserOrder.as_view()),
    path("finalorder/", FinalOrder.as_view())
]
