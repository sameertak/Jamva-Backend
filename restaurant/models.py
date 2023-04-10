from django.db import models
from django.utils import timezone
from userLogin.models import phoneModel

# Create your models here.
class restaurantModel(models.Model):
    resId = models.CharField(blank=False, max_length=6)
    name = models.CharField(blank=False, max_length=25)
    manager = models.CharField(max_length=25)
    contact = models.CharField(max_length=12, blank=False)
    email = models.EmailField(max_length=35)
    social = models.CharField(max_length=50)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.name)

class categoryModel(models.Model):
    resId = models.CharField(max_length=6, blank=False)
    category = models.CharField(max_length=15, blank=False)
    catImage = models.ImageField(default='default.png')

    def __str__(self):
        return str(self.category) + "   (" + str(self.resId) + ")"


class menuModel(models.Model):
    resId = models.CharField(max_length=6, blank=False)
    category = models.CharField(max_length=15, blank=False)
    cat = models.ForeignKey(categoryModel, on_delete=models.CASCADE)
    foodName = models.CharField(max_length=25, blank=False)
    description = models.CharField(max_length=50, default=" ")
    price = models.IntegerField(blank=False)
    ratings = models.IntegerField(default=0)
    counter = models.IntegerField(default=0)
    image = models.ImageField(default='default.png')

    def __str__(self):
        return str(self.foodName)



class orderModel(models.Model):
    customer = models.ForeignKey(phoneModel, on_delete=models.CASCADE)
    userId = models.IntegerField()
    foodId = models.ForeignKey(menuModel, on_delete=models.CASCADE)
    resId = models.CharField(max_length=6)
    quantity = models.IntegerField()
    status = models.BooleanField(default=False)
    price = models.IntegerField()
    info = models.CharField(max_length=50)
    tableNo = models.IntegerField(null=True, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.customer)


class employeeModel(models.Model):
    resId = models.CharField(max_length=6)
    designation = models.CharField(max_length=10)
    name = models.CharField(max_length=25)
    salary = models.CharField(max_length=5)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(null=True)

    def __str__(self):
        return str(self.name)
