from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


def valid_name(value):
    for i in range(len(value)):
        if not value[i].isalnum():
            if not ord(value[i]) == 32:
                raise ValidationError('Value must contain only letters and')
            elif ord(value[i]) == 32 and i <= 1:
                raise ValidationError('Value must contain only letters and')


UserModel = get_user_model()


class CarBrand(models.Model):
    name = models.CharField(max_length=30, validators=(MinLengthValidator(2), valid_name,))
    owner = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)
    status_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class CarModel(models.Model):
    name = models.CharField(max_length=30, validators=(MinLengthValidator(2), valid_name,))
    brand = models.ForeignKey(CarBrand, on_delete=models.CASCADE,)
    owner = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_change = models.DateTimeField(auto_now=True)
    status_delete = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}"


class UserCar(models.Model):
    brand = models.ForeignKey(CarBrand, on_delete=models.SET_NULL, null=True)
    model = models.ForeignKey(CarModel, on_delete=models.SET_NULL, null=True)
    owner = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    status_delete = models.BooleanField(default=False)


