from django.db import models
from userLogin.models import phoneModel

# Create your models here.
class restaurantModel(models.Model):
    name = models.CharField(blank=False, max_length=25)
    manager = models.CharField(max_length=25)
    contact = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length=35)
    social = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)


class menuModel(models.Model):
    resId = models.CharField(max_length=3, blank=False)
    category = models.CharField(max_length=15, blank=False)
    foodName = models.CharField(max_length=25, blank=False)
    description = models.CharField(max_length=50, default='Street Food, Gujarati')
    price = models.IntegerField(blank=False)
    ratings = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)
    image = models.ImageField(default='default.png')

    def __str__(self):
        return str(self.foodName)


class categoryModel(models.Model):
    resId = models.CharField(max_length=3, blank=False)
    category = models.CharField(max_length=15, blank=False)
    catImage = models.ImageField(default='default.png')

    def __str__(self):
        return str(self.category)


class orderModel(models.Model):
    userId = models.IntegerField(default=1)
    foodId = models.IntegerField(default=1)
    resId = models.CharField(default=1, max_length=3)
    quantity = models.IntegerField(default=1)
    status = models.BooleanField(default=False)
    price = models.IntegerField(default=1)

    def __str__(self):
        return str(self.userId)
