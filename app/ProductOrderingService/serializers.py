from rest_framework.serializers import ModelSerializer, CharField, Serializer, EmailField, ValidationError

from ProductOrderingService.models import *
from rest_framework import serializers
from drf_writable_nested.serializers import WritableNestedModelSerializer


class ShopSerializer(ModelSerializer):
    """Класс-сериализатор для получения списка магазинов"""
    class Meta:
        model = Shop
        fields = ('name', 'url', 'state')

class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)


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


class OrderSerializer(WritableNestedModelSerializer):
    ordered_items = OrderItemSerializer(many=True, required=True)

    class Meta:
        model = Order
        fields = [
            "id", "dt", "state", "user", "city", "street", "house", "structure",  "building", "apartment",  "phone",
            "ordered_items"
        ]
        read_only_fields = ["user"]

    # def create(self, validated_data):
    #     """Метод для работы с вложенными сериализаторами"""
    #
    #     order_data = validated_data.pop('ordered_items')
    #     order = Order.objects.create(**validated_data)
    #     for i in order_data:
    #         OrderItem.objects.create(order=order, **i)
    #     return order

    # def update(self, instance, validated_data):
    #
    #     order_data = validated_data.pop('ordered_items')
    #     instance.state = validated_data.get('state', instance.state)
    #     instance.city = validated_data.get('city', instance.city)
    #     instance.street = validated_data.get('street', instance.street)
    #     instance.house = validated_data.get('house', instance.house)
    #     instance.structure = validated_data.get('structure', instance.structure)
    #     instance.building = validated_data.get('building', instance.building)
    #     instance.apartment = validated_data.get('apartment', instance.apartment)
    #     instance.phone = validated_data.get('phone', instance.phone)
    #     instance.save()
    #     for i in order_data:
    #         print(i["quantity"])
    #         i = OrderItem.objects.update(quantity=i["quantity"])
    #         instance.ordered_items.add(i)
    #     return instance


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


