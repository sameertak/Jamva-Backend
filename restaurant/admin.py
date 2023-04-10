from django.contrib import admin
from .models import restaurantModel, menuModel, categoryModel, orderModel, employeeModel

admin.site.register(restaurantModel)
admin.site.register(menuModel)
admin.site.register(categoryModel)
admin.site.register(orderModel)
admin.site.register(employeeModel)