import json
from unittest import TestCase

from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ErrorDetail
from rest_framework.test import APITestCase

from cars.web_car.models import CarBrand, CarModel, valid_name
from cars.web_car.serializers import BrandSerializer, CarModelSerializer


class PermissionAPITestcase(APITestCase, TestCase):
    def setUp(self):
        self.user1 = User.objects.create(username='user1')
        self.user2 = User.objects.create(username='user2')

        self.car_brand1 = CarBrand.objects.create(name='brand1', owner=self.user1)
        self.car_brand2 = CarBrand.objects.create(name='brand2', owner=self.user2)

        self.car_model1 = CarModel.objects.create(name='model1', brand=self.car_brand1)
        self.car_model2 = CarModel.objects.create(name='model2', brand=self.car_brand2)

    def test_permission_get_not_is_authenticated_car_brand(self):
        url = reverse('carbrand-list',)
        response = self.client.get(url)
        serializer = BrandSerializer([self.car_brand1, self.car_brand2], many=True).data
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(serializer, response.data)

    def test_permission_post_is_authenticated_car_brand(self):
        count_brand = CarBrand.objects.all().count()
        self.assertEqual(2, count_brand)

        url = reverse('carbrand-list', )
        self.client.force_login(self.user1)
        data = {
            'name': 'brand3',
        }
        data_json = json.dumps(data)
        response = self.client.post(url, data=data_json, content_type='application/json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        count_brand = CarBrand.objects.all().count()
        self.assertEqual(3, count_brand)

    def test_permission_put_is_authenticated_car_brand(self):
        url = reverse('carbrand-detail', args=(self.car_brand1.id,))
        self.client.force_login(self.user1)
        data = {
            'name': 'put brand',
        }
        data_json = json.dumps(data)
        response = self.client.put(url, data=data_json, content_type='application/json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.car_brand1 = CarBrand.objects.get(id=self.car_brand1.id)
        self.assertEqual(data['name'], self.car_brand1.name)

    def test_permission_put_is_not_authenticated_car_brand(self):
        url = reverse('carbrand-detail', args=(self.car_brand2.id,))
        data = {
            'name': 'put',
        }
        data_json = json.dumps(data)
        self.client.put(self.user1)
        response = self.client.put(url, data=data_json, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        self.car_brand2 = CarBrand.objects.get(id=self.car_brand2.id)
        self.assertEqual('brand2', self.car_brand2.name)
        self.assertEqual({'detail': ErrorDetail(string='Authentication credentials were not provided.',
                                                code='not_authenticated')}, response.data)

    def test_permission_delete_is_authenticated_car_brand(self):
        count_brand = CarBrand.objects.all().count()
        self.assertEqual(2, count_brand)

        url = reverse('carbrand-detail', args=(self.car_brand1.id,))
        self.client.force_login(self.user1)

        response = self.client.delete(url, data=self.car_brand1, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        count_brand = CarBrand.objects.all().count()
        self.assertEqual(2, count_brand)

        CarBrand.refresh_from_db(self.car_brand1)
        self.assertTrue(self.car_brand1.status_delete)

    def test_permission_delete_is_not_authenticated_car_brand(self):
        count_brand = CarBrand.objects.all().count()
        self.assertEqual(2, count_brand)

        url = reverse('carbrand-detail', args=(self.car_brand1.id,))
        self.client.force_login(self.user2)
        response = self.client.delete(url, data=self.car_brand1, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)

        count_brand = CarBrand.objects.all().count()
        self.assertEqual(2, count_brand)

        self.assertFalse(self.car_brand1.status_delete)

    def test_permission_get_not_is_authenticated_car_model(self):
        url = reverse('carmodel-list',)
        serializer = CarModelSerializer([self.car_model1, self.car_model2], many=True).data

        response = self.client.get(url,)

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual(response.data, serializer)

    def test_permission_post_is_authenticated_car_model(self):
        count_model = CarModel.objects.all().count()
        self.assertEqual(2, count_model)

        url = reverse('carmodel-list',)
        data = {
            'name': 'model test',
            'brand': self.car_brand1.id,
        }
        data_json = json.dumps(data)

        self.client.force_login(self.user1)
        response = self.client.post(url, data=data_json, content_type='application/json')

        self.assertEqual(status.HTTP_201_CREATED, response.status_code)

        count_model = CarModel.objects.all().count()
        self.assertEqual(3, count_model)

    def test_permission_post_is_not_authenticated_car_model(self):
        count_model = CarModel.objects.all().count()
        self.assertEqual(2, count_model)

        url = reverse('carmodel-list')
        data = {
            'name': 'car_model3',
            'brand': self.car_brand1.id,
        }
        data_json = json.dumps(data)

        response = self.client.post(url, data=data_json, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)

        count_model = CarModel.objects.all().count()
        self.assertEqual(2, count_model)

    def test_permission_delete_is_authenticated_car_model(self):
        count_model = CarModel.objects.all().count()
        self.assertEqual(2, count_model)

        url = reverse('carmodel-detail', args=(self.car_model1.id,))

        self.client.force_login(self.user1)
        response = self.client.delete(url, data=self.car_model1, content_type='application/json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        CarBrand.refresh_from_db(self.car_model1)

        count_model = CarModel.objects.all().count()
        self.assertEqual(2, count_model)

        self.assertTrue(self.car_model1.status_delete)

    def test_permission_delete_is_not_authenticated_car_model(self):
        count_model = CarModel.objects.all().count()
        self.assertEqual(2, count_model)

        url = reverse('carmodel-detail', args=(self.car_model1.id,))

        response = self.client.delete(url, data=self.car_model1, content_type='application/json')
        self.assertEqual(status.HTTP_403_FORBIDDEN, response.status_code)
        CarBrand.refresh_from_db(self.car_model1)

        count_model = CarModel.objects.all().count()
        self.assertEqual(2, count_model)

        self.assertFalse(self.car_model1.status_delete)

    def test_func_auth(self):
        url = reverse('auth')
        response = self.client.get(url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)

    def test_valid_name(self):
        value = '  test'
        value2 = '%test'
        with self.assertRaises(Exception) as ex:
            valid_name(value)
        self.assertEqual('Value must contain only letters and', str(ex.exception.message))
        with self.assertRaises(Exception) as ex:
            valid_name(value2)
        self.assertEqual('Value must contain only letters and', str(ex.exception.message))