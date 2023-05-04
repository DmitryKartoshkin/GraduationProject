from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from requests import get
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny
from rest_framework import filters
from rest_framework import status
from rest_framework.generics import CreateAPIView

from rest_framework.permissions import AllowAny

from yaml import load as load_yaml, Loader, safe_load

from ProductOrderingService.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, User
from ProductOrderingService.serializers import ProductSerializer, OrderSerializer, UserSerializer, UserRegistrSerializer
from pathlib import Path


class UploadViewSet(APIView):
    """Класс для загрузки информации о товарах в БД интернет-магазина"""
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        #
        # if request.user.type != 'shop':
        #     return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        file = request.data.get("File")
        if file:
            if Path(file.name).suffix[1:].lower() == 'yaml':
                data = load_yaml(file, Loader=Loader)
                shop, _ = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)

                for category in data['categories']:
                    category_object, _ = Category.objects.get_or_create(id=category['id'], name=category['name'])
                    category_object.shops.add(shop.id)
                    category_object.save()
                ProductInfo.objects.filter(shop_id=shop.id).delete()
                for item in data['goods']:
                    product, _ = Product.objects.get_or_create(name=item['name'], category_id=item['category'])
                    product_info = ProductInfo.objects.create(product_id=product.id,
                                                              external_id=item['id'],
                                                              model=item['model'],
                                                              price=item['price'],
                                                              price_rrc=item['price_rrc'],
                                                              quantity=item['quantity'],
                                                              shop_id=shop.id)
                    for name, value in item['parameters'].items():
                        parameter_object, _ = Parameter.objects.get_or_create(name=name)
                        ProductParameter.objects.create(product_info_id=product_info.id,
                                                        parameter_id=parameter_object.id,
                                                        value=value)

                return JsonResponse({'Status': True})
            else:
                raise ValidationError(message={"Error"})

# class ProductView(APIView):
#     def get(self, request):
#         queryset = Product.objects.all()
#         data = ProductSerializer(queryset, many=True).data
#         return Response(data)
#
#         # queryset = Product.objects.all().values()
#         # return Response({'Products': list(queryset)})
#         # return JsonResponse({'Products': list(queryset)})


class ProductViewSet(ModelViewSet):
    """Класс для просмотра продуктов интернет-магазина"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)


class OrderViewSet(ModelViewSet):
    """Класс для работы с заказами интернет-магазина"""
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    # permission_classes = (IsAuthenticatedOrReadOnly,)


class RegistrUserView(CreateAPIView):
# class RegistrUserView(ModelViewSet):
    """Класс для создания пользователей"""
    queryset = User.objects.all()
    serializer_class = UserRegistrSerializer
    # Добавляем права доступа
    permission_classes = [AllowAny]

    # Создаём метод для создания нового пользователя
    def post(self, request, *args, **kwargs):
        # Добавляем UserRegistrSerializer
        serializer = UserRegistrSerializer(data=request.data)
        # Создаём список data
        data = {}
        # Проверка данных на валидность
        if serializer.is_valid():
            # Сохраняем нового пользователя
            serializer.save()
            # Добавляем в список значение ответа True
            data['response'] = True
            # Возвращаем что всё в порядке
            return Response(data, status=status.HTTP_200_OK)
        else:  # Иначе
            # Присваиваем data ошибку
            data = serializer.errors
            # Возвращаем ошибку
            return Response(data)
