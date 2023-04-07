from django.contrib import admin
from .models import restaurantModel, menuModel, categoryModel, orderModel

admin.site.register(restaurantModel)
admin.site.register(menuModel)
admin.site.register(categoryModel)
admin.site.register(orderModel)