from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth-login-logout/', include('rest_framework.urls')),
    path('github-authentication/', include('cars.web_car.urls')),
    path('cars/', include('cars.web_car.urls')),
    path('', include('social_django.urls', namespace='social')),

]


