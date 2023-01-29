from rest_framework import serializers
from .models import menuModel, restaurantModel, categoryModel, orderModel
from django.db import models


class MenuSerializers(serializers.ModelSerializer):
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


class RestaurantSerializers(serializers.ModelSerializer):
    name = models.CharField(blank=False, max_length=25)
    manager = models.CharField(max_length=25)
    contact = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length=35)
    social = models.CharField(max_length=50)

    class Meta:
        model = restaurantModel
        fields = ('name', 'manager', 'contact', 'email', 'social')


class CategorySerializers(serializers.ModelSerializer):
    category = models.CharField(max_length=15, blank=False)
    catImage = models.ImageField(default='default.png', null=False)

    class Meta:
        model = categoryModel
        fields = '__all__'


class CategoryMenuSerializers(serializers.ModelSerializer):
    foodName = models.CharField(max_length=25, blank=False)
    description = models.CharField(max_length=50)
    price = models.IntegerField(blank=False)
    ratings = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)
    image = models.ImageField(default='default.png')

    class Meta:
        model = menuModel
        fields = ('id', 'foodName', 'price', 'ratings', 'counter', 'image', 'description')


class OrderSerializers(serializers.ModelSerializer):
    quantity = models.IntegerField()
    price = models.IntegerField()

    class Meta:
        model = orderModel
        fields = ('quantity', 'price')


class FinalOrderSerializers(serializers.ModelSerializer):
    foodId = models.IntegerField()
    quantity = models.IntegerField()
    status = models.BooleanField()

    class Meta:
        model = orderModel
        fields = ('foodId', 'quantity', 'status')