from rest_framework import serializers

from userLogin.models import phoneModel
from .models import menuModel, restaurantModel, categoryModel, orderModel, employeeModel
from django.db import models


class RestaurantSerializers(serializers.ModelSerializer):
    name = models.CharField(blank=False, max_length=25)
    manager = models.CharField(max_length=25)
    contact = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length=35)
    social = models.CharField(max_length=50)

    class Meta:
        model = restaurantModel
        fields = '__all__'


class CategorySerializers(serializers.ModelSerializer):
    category = models.CharField(max_length=15, blank=False)
    catImage = models.ImageField(default='default.png', null=False)

    class Meta:
        model = categoryModel
        fields = '__all__'


class CategoryMenuSerializers(serializers.ModelSerializer):
    # cat = CategorySerializers()
    foodName = models.CharField(max_length=25, blank=False)
    description = models.CharField(max_length=50)
    price = models.IntegerField(blank=False)
    ratings = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)
    image = models.ImageField(default='default.png')

    class Meta:
        model = menuModel
        fields = '__all__'


class MenuSerializers(serializers.ModelSerializer):
    category = CategorySerializers()
    resId = models.CharField(max_length=3, blank=False)
    category = models.CharField(max_length=15, blank=False)
    foodName = models.CharField(max_length=25, blank=False)
    price = models.IntegerField(blank=False)
    ratings = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)
    image = models.ImageField(default='default.png')
    name = models.CharField(blank=False, max_length=25)

    class Meta:
        model = menuModel
        fields = '__all__'

class OrderSerializers(serializers.ModelSerializer):
    quantity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        model = orderModel
        fields = ('quantity', 'price')


class MenuManageSerializers(serializers.ModelSerializer):
    # details = serializers.CharField(max_length=200)

    class Meta:
        model = menuModel
        fields = '__all__'

class FinalOrderSerializers(serializers.ModelSerializer):
    foodId = MenuSerializers()
    quantity = models.IntegerField()
    status = models.BooleanField()
    info = models.CharField(max_length=50)
    class Meta:
        model = orderModel
        fields = ('id', 'foodId', 'quantity', 'status', 'info', 'updated_at')


class CustomerSerializers(serializers.ModelSerializer):
    name = models.CharField(blank=False, max_length=15)
    mobile = models.CharField(max_length=13, blank=False)

    class Meta:
        model = phoneModel
        fields = ('name', 'mobile')


class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializers()
    foodId = MenuSerializers()

    class Meta:
        model = orderModel
        fields = ('userId', 'resId', 'quantity', 'status', 'price', 'customer', 'foodId', 'created_at', 'updated_at')


class OrderCustomerSerializer(serializers.ModelSerializer):
    customer = CustomerSerializers()
    foodId = MenuSerializers()
    total_quantity = serializers.IntegerField(read_only=True)

    class Meta:
        model = orderModel
        fields = ('userId', 'resId', 'quantity', 'status', 'price', 'customer', 'foodId', 'created_at', 'updated_at', 'total_quantity')

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['total_quantity'] = instance.total_quantity
        return representation

class RestaurantDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model=restaurantModel
        fields='__all__'

class TotalPriceSerializers(serializers.ModelSerializer):
    total_price = serializers.IntegerField(read_only=True)
    total_quantity = serializers.IntegerField(read_only=True)
    class Meta:
        model = orderModel
        fields = ('total_price', 'total_quantity')


class EmployeeSerializers(serializers.ModelSerializer):
    class Meta:
        model = employeeModel
        fields = '__all__'