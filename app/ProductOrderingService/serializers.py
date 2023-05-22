from rest_framework.serializers import ModelSerializer, CharField, Serializer, EmailField, ValidationError

from ProductOrderingService.models import *
from rest_framework import serializers

from drf_writable_nested.serializers import WritableNestedModelSerializer


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class ShopSerializer(ModelSerializer):
    """Класс-сериализатор для получения списка магазинов"""
    class Meta:
        model = Shop
        fields = ('id', 'name', 'url', 'state')
        read_only_fields = ('id',)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)

#
# class OrderItemSerializer(ModelSerializer):
#
#     class Meta:
#         model = OrderItem
#         fields = ["id", "quantity", "product_info"]


# class OrderSerializer(WritableNestedModelSerializer):
#     ordered_items = OrderItemSerializer(many=True, required=True)
#
#     class Meta:
#         model = Order
#         fields = [
#             "id", "dt", "state", "user", "city", "street", "house", "structure",  "building", "apartment",  "phone",
#             "ordered_items"
#         ]
#         read_only_fields = ["user"]

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

# class OrderSerializer(ModelSerializer):
# class OrderSerializer(WritableNestedModelSerializer):
#
#     ordered_items = OrderItemSerializer(many=True, required=True)
#
#     class Meta:
#         model = Order
#         fields = '__all__'
#         read_only_fields = ["user"]

    # def create(self, validated_data):
    #     """Метод для работы с вложенными сериализаторами"""
    #     order_data = validated_data.pop('ordered_items')
    #
    #     order = Order.objects.create(**validated_data)
    #     for i in order_data:
    #         OrderItem.objects.create(order=order, **i)
    #     return order

    # def update(self, instance, validated_data):
    #     order_data = validated_data.pop('ordered_items')
    #     ordered_items = instance.ordered_items
    #     instance.state = validated_data.get('state', instance.state)
    #     instance.save()
    #     return instance


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "username", "password", "first_name", "last_name", "username", "company", "position"]


class UserRegistrSerializer(ModelSerializer):
    """Класс сериализации для модели User для регистрации"""
    # Поле для повторения пароля
    password2 = serializers.CharField()

    class Meta:
        model = User
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


class ProductSerializer(ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Product
        fields = ('name', 'category',)


class ProductParameterSerializer(serializers.ModelSerializer):
    parameter = serializers.StringRelatedField()

    class Meta:
        model = ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(ModelSerializer):

    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters',)
        read_only_fields = ('id',)


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ('id', 'product_info', 'quantity', 'order',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }

class OrderItemCreateSerializer(OrderItemSerializer):

    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(serializers.ModelSerializer):

    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)
    contact = ContactSerializer()
    # state = serializers.StringRelatedField(default="new")

    class Meta:
        model = Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'contact',)
        read_only_fields = ('id',)

    # def update(self, instance, validated_data):
    #     # contact_data = validated_data.pop('contact')
    #     # print(contact_data)
    #     # contact = instance.contact
    #     # print(contact)
    #
    #     instance.contact = validated_data.get('contact', instance.contact)
    #     instance.state = validated_data.get('state', instance.state)
    #     instance.save()

        # contact.city = contact_data.get('city', contact.city)
        # contact.street = contact_data.get('street', contact.street)
        # contact.house = contact_data.get('house', contact.house)
        # contact.structure = contact_data.get('structure', contact.structure)
        # contact.building = contact_data.get('building', contact.building)
        # contact.apartment = contact_data.get('apartment', contact.apartment)
        # contact.phone = contact_data.get('phone', contact.phone)
        # contact.save()
        # return instance



