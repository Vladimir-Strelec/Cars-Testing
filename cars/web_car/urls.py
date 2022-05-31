from django.urls import path
from rest_framework import routers
from cars.web_car.views import CarBrandView, CarModelView, UserCarView, auth

router = routers.SimpleRouter()
router.register(r'car/brand', CarBrandView)
router.register(r'car/model', CarModelView)
router.register(r'user/car', UserCarView)

urlpatterns = [
    path('git/', auth, name='auth')
]
urlpatterns += router.urls
