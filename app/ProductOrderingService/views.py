from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.views import APIView
from django.http import JsonResponse, Http404
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.forms import model_to_dict
from rest_framework import filters
from rest_framework import status, mixins

from yaml import load as load_yaml, Loader

from ProductOrderingService.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter, Order, \
    User, OrderItem, Contact

from ProductOrderingService.serializers import OrderSerializer, OrderItemSerializer, ShopSerializer, \
    CategorySerializer, ProductSerializer, ContactSerializer


class UploadViewSet(APIView):
    """Класс для загрузки информации о товарах в БД интернет-магазина"""
    def post(self, request, *args, **kwargs):
        """
        Метод для загрузки каталога товаров по каждому магазину.

        Принимает yaml-файл в качестве аргумента.
        """
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        file = request.data.get("File")
        if file:
            validate_file = FileExtensionValidator(['yaml'])
            try:
                validate_file(file)
            except ValidationError as e:
                return JsonResponse({'Status': False, 'Error': str(e)})
            else:
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
        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ShopViewSet(GenericViewSet, mixins.ListModelMixin):
    """Класс для просмотра списка интернет-магазина"""
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


class CategoriesViewSet(GenericViewSet, mixins.ListModelMixin):
    """Класс для просмотра списка категорий"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class ProductViewSet(GenericViewSet, mixins.ListModelMixin, mixins.RetrieveModelMixin):
    """Класс для просмотра продуктов интернет-магазина"""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# class BasketViewSet(ModelViewSet):
#     """Класс для работы с заказами интернет-магазина.
#     """
#     queryset = Order.objects.all()
#     serializer_class = OrderSerializer
#     permission_classes = (IsOwner, )
#
#     def get_queryset(self):
#         """Метод вывотит заказы конкретного пользователя исходя из переданного токена"""
#         queryset = self.queryset
#         query_set = queryset.filter(user=self.request.user)
#         return query_set
#
#     def perform_create(self, serializer):
#         """Метод позволяет автоматически заполнить поля user при создании заказа исходя из переданного токена"""
#         serializer.save(user=self.request.user)


# class RegistrUserView(CreateAPIView):
#     """Класс для создания пользователей"""
#     queryset = User.objects.all()
#     serializer_class = UserRegistrSerializer
#     permission_classes = [AllowAny]
#
#     # Создаём метод для создания нового пользователя
#     def post(self, request, *args, **kwargs):
#         # Добавляем UserRegistrSerializer
#         serializer = UserRegistrSerializer(data=request.data)
#         # Создаём список data
#         data = {}
#         # Проверка данных на валидность
#         if serializer.is_valid():
#             # Сохраняем нового пользователя
#             serializer.save()
#             # Добавляем в список значение ответа True
#             data['response'] = True
#             # Возвращаем что всё в порядке
#             return Response(data, status=status.HTTP_200_OK)
#         else:
#             # Присваиваем data ошибку
#             data = serializer.errors
#             # Возвращаем ошибку
#             return Response(data)


class BasketView(APIView):
    """Класс для работы со списком заказов"""

    def get(self, request, *args, **kwargs):
        """Метод для просмотра списка заказов"""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        basket = Order.objects.filter(
            user_id=request.user.id, state='basket').prefetch_related(
            'ordered_items__product_info__product__category',
            'ordered_items__product_info__product_parameters__parameter').distinct()
        serializer = OrderSerializer(basket, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Метод для создания заказа"""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        items_dict = request.data.get('ordered_items')
        if items_dict:
            basket = Order.objects.create(user_id=request.user.id, state='basket')
            for order_item in items_dict:
                order_item.update({'order': basket.id})
                serializer = OrderItemSerializer(data=order_item)
                if serializer.is_valid():
                    serializer.save()
                else:
                    return JsonResponse({'Status': False, 'Errors': serializer.errors})
            return JsonResponse({'Status': True, 'Создано объектов': model_to_dict(basket)})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class BasketViewDetail(APIView):
    """Класс для работы с карточкой заказа"""

    def get(self, request, *args, **kwargs):
        """Метод для просмотра карточки заказов."""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        pk = kwargs.get('pk', None)
        if not pk:
            return JsonResponse({'Error': 'Method DELETE not allowed'}, status=403)
        else:
            basket = Order.objects.filter(
                user_id=request.user.id, state='basket', id=pk).prefetch_related(
                'ordered_items__product_info__product__category',
                'ordered_items__product_info__product_parameters__parameter').distinct()
            serializer = OrderSerializer(basket, many=True)
            return Response(serializer.data)

    def put(self, request, *args, **kwargs):
        """Метод для обновления или добавления продуктов к заказу."""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        pk = kwargs.get('pk', None)
        if not pk:
            return JsonResponse({'Error': 'Method PUT not allowed'}, status=403)

        items_dict = request.data.get('ordered_items')
        if items_dict:
            for order_item in items_dict:
                if order_item.get('id') is None:
                    order_item.update(order=pk)
                    serializer = OrderItemSerializer(data=order_item)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return JsonResponse({'Status': False, 'Errors': serializer.errors})
                else:
                    items = OrderItem.objects.filter(id=order_item['id']).update(
                        quantity=order_item['quantity'],
                        product_info=order_item["product_info"]
                    )
            return JsonResponse({'Status': True})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})

    def delete(self, request, *args, **kwargs):
        """Метод для удаления заказа."""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        pk = kwargs.get('pk', None)
        if not pk:
            return JsonResponse({'Error': 'Method DELETE not allowed'}, status=403)

        order = Order.objects.filter(user_id=request.user.id, id=pk)
        if order.first() is None:
            return JsonResponse({'Error': 'Method DELETE  is not applicable to the specified object'}, status=403)
        else:
            order.delete()
            return JsonResponse({'Status': True, 'Answer': 'Order delete'}, status=status.HTTP_204_NO_CONTENT)


class PartnerOrders(APIView):
    """Класс для получения заказов поставщиками"""

    def get(self, request, *args, **kwargs):
        """Метод для получения списка заказов магазина"""

        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if request.user.type != 'shop':
            return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)

        order = Order.objects.filter(
            ordered_items__product_info__shop__user_id=request.user.id).exclude(state='basket'). \
            prefetch_related('ordered_items__product_info__product__category',
                             'ordered_items__product_info__product_parameters__parameter'). \
            select_related('contact').distinct()
        serializer = OrderSerializer(order, many=True)
        return Response(serializer.data)


class ContactAllView(APIView):
    """Класс для работы с контактами покупателей"""

    def get(self, request, *args, **kwargs):
        """Класс для просмотра списка контактов"""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        contact = Contact.objects.filter(user_id=request.user.id)
        serializer = ContactSerializer(contact, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Класс для создания контакта"""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        if {'city', 'street', 'phone', 'house'}.issubset(request.data):
            request.data.update({'user': request.user.id})
            serializer = ContactSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True})
            else:
                return JsonResponse({'Status': False, 'Errors': serializer.errors})

        return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ContactView(APIView):
    """Класс для работы с указанным контактом"""

    def get(self, request, *args, **kwargs):
        """Метод для просмотра карточки контакта"""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        pk = kwargs.get('pk', None)
        if not pk:
            return JsonResponse({'Error': 'Method DELETE not allowed'}, status=403)
        else:
            contact = Contact.objects.filter(id=pk)
            serializer = ContactSerializer(contact, many=True)
            return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        """Метод для удаления контакта"""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        pk = kwargs.get('pk', None)
        if not pk:
            return JsonResponse({'Error': 'Method DELETE not allowed'}, status=403)

        contact = Contact.objects.filter(user_id=request.user.id, id=pk)
        if contact.first() is None:
            return JsonResponse({'Error': 'Method DELETE  is not applicable to the specified object'}, status=403)
        else:
            contact.delete()
            return JsonResponse({'Status': True, 'Answer': 'Contact delete'}, status=status.HTTP_204_NO_CONTENT)

    #  редактировать контакт
    def put(self, request, *args, **kwargs):
        """Метод для обновления данных в контакте"""
        if not request.user.is_authenticated:
            return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)
        pk = kwargs.get('pk', None)

        if not pk:
            return JsonResponse({'Error': 'Method DELETE not allowed'}, status=403)

        if 'id' in request.data:
            contact = Contact.objects.filter(user_id=request.user.id, id=pk).first()
            serializer = ContactSerializer(contact, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse({'Status': True, 'Answer': serializer.data})
        else:
            return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})
