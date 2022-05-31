from django.contrib import admin

from cars.web_car.models import UserCar, CarModel, CarBrand


@admin.register(CarBrand)
class CarBrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'owner', 'date_created', 'date_change']


@admin.register(CarModel)
class CarModelAdmin(admin.ModelAdmin):
    list_display = ['name', 'brand', 'date_created', 'date_change']


@admin.register(UserCar)
class UserCarAdmin(admin.ModelAdmin):
    pass


