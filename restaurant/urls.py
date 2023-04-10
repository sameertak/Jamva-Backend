from django.contrib import admin
from django.urls import path, include
from .views import RestMenu, RestDetail, DeleteItem, AvailabeCategory, AddMenu, CategoryMenu, UserOrder, FinalOrder, \
    SetStatus, AllRestaurants, GetRestaurantNameById, RegisterRestaurant, CustomerList, UpdateItem, UserDetail, \
    NameToIdCat, ManageMenu, FoodMenu, UpdateMenuItem, DeleteMenuItem, RestaurantDetail, CheckStatus, CardPayment, \
    GetTotalPrice, \
    UpdateItemStatus, TrendingItem, ConfmOrder, RestaurantDetailsAPI, EmployeeDetail, EmployeeAdd, EmployeeGet, \
    EmployeeEdit, EmployeeDelete, SetTableNo

urlpatterns = [
    path("menu/", RestMenu.as_view()),
    path("detail/", RestDetail.as_view()),
    path("category/", AvailabeCategory.as_view()),
    path("menu/add/", AddMenu.as_view()),           #Changed catId
    path("menu/category/", CategoryMenu.as_view()),  #Changed catId
    path("order/", UserOrder.as_view()),
    path("finalorder/", FinalOrder.as_view()),
    path("all/", AllRestaurants.as_view()),
    path("get/", GetRestaurantNameById.as_view()),
    path("add/restaurant/", RegisterRestaurant.as_view()),
    path('customers/', CustomerList.as_view()),
    path('order/update/', UpdateItem.as_view()),
    path('order/delete/', DeleteItem.as_view()),
    path('order/userdetail', UserDetail.as_view()),
    path('ntc/', NameToIdCat.as_view()),
    path('menu/manage/', ManageMenu.as_view()),
    path('menu/id',FoodMenu.as_view()),
    path('menu/update', UpdateMenuItem.as_view()),
    path('menu/delete', DeleteMenuItem.as_view()),
    path('details/', RestaurantDetail.as_view()),
    path('set/status/', SetStatus.as_view()),
    path('check/status/', CheckStatus.as_view()),
    path('payment/', CardPayment.as_view()),
    path('totalprice/', GetTotalPrice.as_view()),
    path('update/status/', UpdateItemStatus.as_view()),
    path('trending/', TrendingItem.as_view()),
    path('table/', SetTableNo.as_view()),
    path('user/order/', ConfmOrder.as_view()),
    path('fullDetails/', RestaurantDetailsAPI.as_view()),
    path('employees/', EmployeeDetail.as_view()),
    path('add/employee/', EmployeeAdd.as_view()),
    path('get/employee/', EmployeeGet.as_view()),
    path('edit/employee/', EmployeeEdit.as_view()),
    path('delete/employee/', EmployeeDelete.as_view()),
]
