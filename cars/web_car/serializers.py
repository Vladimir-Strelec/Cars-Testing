from rest_framework.serializers import ModelSerializer

from cars.web_car.models import UserCar, CarBrand, CarModel


class BrandSerializer(ModelSerializer):
    class Meta:
        model = CarBrand
        fields = ('name',)


class CarModelSerializer(ModelSerializer):
    class Meta:
        model = CarModel
        fields = ('name', 'brand')


class UserCarSerializer(ModelSerializer):
    class Meta:
        model = UserCar
        fields = ('brand', 'model')
