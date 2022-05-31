import json

from django.test import TestCase
from rest_framework import status


from cars.web_car.models import CarBrand, CarModel, UserCar
from cars.web_car.serializers import BrandSerializer, CarModelSerializer, UserCarSerializer


class TestBrandSerializer(TestCase):
    def test_valid_data_brand(self):
        brand1 = CarBrand.objects.create(name='Brand')
        brand2 = CarBrand.objects.create(name='Brand2')
        serializer_data = BrandSerializer([brand1, brand2], many=True).data

        data = [
            {
                'name': 'Brand'
            },
            {
                'name': 'Brand2'
            }
        ]
        self.assertEqual(data, serializer_data)

    def test_valid_data_model(self):
        brand = CarBrand.objects.create(name='Brand')
        model1 = CarModel.objects.create(name='Model', brand=brand)
        model2 = CarModel.objects.create(name='Model2', brand=brand)
        serializer_data = CarModelSerializer([model1, model2], many=True).data

        data = [
            {
                "name": model1.name,
                "brand": model1.brand.id
            },
            {
                "name": model2.name,
                "brand": model2.brand.id
            }
        ]
        self.assertEqual(data, serializer_data)

    def test_valid_data_user_car(self):
        brand = CarBrand.objects.create(name='Brand')
        model = CarModel.objects.create(name='Model', brand=brand)
        user_car1 = UserCar.objects.create(brand=brand, model=model)
        user_car2 = UserCar.objects.create(brand=brand, model=model)
        serializer = UserCarSerializer([user_car1, user_car2], many=True).data
        data = [
            {
                'brand': brand.id,
                'model': model.id,
             },
            {
                'brand': brand.id,
                'model': model.id,
            }
        ]
        self.assertEqual(data, serializer)
