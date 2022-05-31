from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import viewsets, status
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from cars.web_car.models import CarBrand, CarModel, UserCar
from cars.web_car.permission import CustomAuthenticated
from cars.web_car.serializers import BrandSerializer, CarModelSerializer, UserCarSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication




class CarBrandView(viewsets.ModelViewSet):
    queryset = CarBrand.objects.all()
    serializer_class = BrandSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [CustomAuthenticated]

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filter_fields = ['name']
    search_filter = ['owner']
    ordering_filter = ['name']


    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        model = CarBrand.objects.get(id=kwargs['pk'])
        model.status_delete = True
        model.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class CarModelView(viewsets.ModelViewSet):
    queryset = CarModel.objects.filter(status_delete=False)
    serializer_class = CarModelSerializer
    # authentication_classes = [SessionAuthentication, BasicAuthentication]

    permission_classes = [IsAuthenticatedOrReadOnly, CustomAuthenticated]

    def perform_create(self, serializer):
        serializer.validated_data['owner'] = self.request.user
        serializer.save()

    def destroy(self, request, *args, **kwargs):
        model = CarModel.objects.get(id=kwargs['pk'])
        model.status_delete = True
        model.save()
        return Response(status=status.HTTP_204_NO_CONTENT)


class UserCarView(viewsets.ModelViewSet):
    queryset = UserCar.objects.all()
    serializer_class = UserCarSerializer
    permission_classes = [CustomAuthenticated]


def auth(request):
    return render(request, 'oauth.html')
