from rest_framework.serializers import ModelSerializer, CharField, Serializer, EmailField, ValidationError

from ProductOrderingService.models import *
from rest_framework import serializers
# from .models import User


# class ShopSerializer(ModelSerializer):
#     class Meta:
#         model = Shop
#         fields = ('name', 'url', 'state')

# class CategorySerializer(ModelSerializer):
#     class Meta:
#         model = Category
#         fields = ('name', )


# class ContactSerializer(ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = ('city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')
#
# class OrderSerializer(ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ('state', 'contact')
#
# class OrderItemSerializer(ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ('quantity',)

class ParameterSerializer(ModelSerializer):
    class Meta:
        model = Parameter
        # fields = ["id", "name"]
        fields = '__all__'


class ProductParameterSerializer(ModelSerializer):
    # parameter = ParameterSerializer(many=True, required=False)
    class Meta:
        model = ProductParameter
        fields = ["id", "value", "parameter"]


class ProductInfoSerializer(ModelSerializer):
    product_parameters = ProductParameterSerializer(many=True, required=False)

    class Meta:
        model = ProductInfo
        fields = ["id", "external_id", "model", "quantity", "price", "price_rrc", "product_parameters"]


class ProductSerializer(ModelSerializer):
    product_infos = ProductInfoSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = ["id", "name", "product_infos", "category"]


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "quantity", "product_info"]


class OrderSerializer(ModelSerializer):
    ordered_items = OrderItemSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "dt", "state", "user", "city", "street", "house", "structure",  "building", "apartment",  "phone",
            "ordered_items"
        ]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "first_name", "last_name", "username", "company", "position"]


class UserRegistrSerializer(ModelSerializer):
    """Класс сериализации для модели User"""
    # Поле для повторения пароля
    password2 = serializers.CharField()

    class Meta:
        # Поля модели которые будем использовать
        model = User
        # Назначаем поля которые будем использовать
        fields = [
            'email', 'username', 'first_name', 'last_name', 'company', 'position', 'type', 'password', 'password2'
        ]

    def save(self, *args, **kwargs):
        """Метод создания объекта класса User"""
        user = User(
            email=self.validated_data['email'],  # Назначаем Email
            username=self.validated_data['username'],  # Назначаем Логин
            first_name=self.validated_data['first_name'],  # Назначаем Имя
            last_name=self.validated_data['last_name'],  # Назначаем Фамилию
            company=self.validated_data['company'],  # Назначаем Компанию
            position=self.validated_data['position'],  # Назначаем Должность
            type=self.validated_data['type'],  # Назначаем Тип пользователя
        )
        # Проверяем на валидность пароль
        password = self.validated_data['password']
        # Проверяем на валидность повторный пароль
        password2 = self.validated_data['password2']
        # Проверяем совпадают ли пароли
        if password != password2:
            # Если нет, то выводим ошибку
            raise serializers.ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user

# class PollSerializer(ModelSerializer):
#     choices = ChoiceSerializer(many=True, read_only=True, required=False)
#
#     class Meta:
#         model = Poll
#         fields = '__all__'
