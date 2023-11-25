from rest_framework.serializers import ModelSerializer, CharField, Serializer, EmailField, ValidationError,\
    StringRelatedField, PrimaryKeyRelatedField

from ProductOrderingService import models


class ContactSerializer(ModelSerializer):
    class Meta:
        model = models.Contact
        fields = ('id', 'city', 'street', 'house', 'structure', 'building', 'apartment', 'user', 'phone')
        read_only_fields = ('id',)
        extra_kwargs = {
            'user': {'write_only': True}
        }


class ShopSerializer(ModelSerializer):
    """Класс-сериализатор для получения списка магазинов"""
    class Meta:
        model = models.Shop
        fields = ('id', 'name', 'url', 'state')
        read_only_fields = ('id',)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = models.Category
        fields = ('id', 'name',)
        read_only_fields = ('id',)


class UserSerializer(ModelSerializer):
    class Meta:
        model = models.User
        fields = ["id", "email", "username", "password", "first_name", "last_name", "username", "company", "position"]


class UserRegistrSerializer(ModelSerializer):
    """Класс-сериализатор для модели User для регистрации"""
    # Поле для повторения пароля
    password2 = CharField()

    class Meta:
        model = models.User
        fields = [
            'email', 'username', 'first_name', 'last_name', 'company', 'position', 'type', 'password', 'password2'
        ]

    def save(self, *args, **kwargs):
        """Метод создания объекта класса User"""
        user = models.User(
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
            raise ValidationError({password: "Пароль не совпадает"})
        # Сохраняем пароль
        user.set_password(password)
        # Сохраняем пользователя
        user.save()
        # Возвращаем нового пользователя
        return user


class ProductSerializer(ModelSerializer):
    category = StringRelatedField()

    class Meta:
        model = models.Product
        fields = ('name', 'category',)


class ProductParameterSerializer(ModelSerializer):
    parameter = StringRelatedField()

    class Meta:
        model = models.ProductParameter
        fields = ('parameter', 'value',)


class ProductInfoSerializer(ModelSerializer):

    product = ProductSerializer(read_only=True)
    product_parameters = ProductParameterSerializer(read_only=True, many=True)

    class Meta:
        model = models.ProductInfo
        fields = ('id', 'model', 'product', 'shop', 'quantity', 'price', 'price_rrc', 'product_parameters',)
        read_only_fields = ('id',)


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = models.OrderItem
        fields = ('id', 'product_info', 'quantity', 'order',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'order': {'write_only': True}
        }


class OrderItemCreateSerializer(OrderItemSerializer):

    product_info = ProductInfoSerializer(read_only=True)


class OrderSerializer(ModelSerializer):

    ordered_items = OrderItemCreateSerializer(read_only=True, many=True)
    contact = ContactSerializer(read_only=True)
    contact_id = PrimaryKeyRelatedField(
        write_only=True, source="contact",
        queryset=models.Contact.objects.all()
    )
    state = StringRelatedField(default="new")

    class Meta:
        model = models.Order
        fields = ('id', 'ordered_items', 'state', 'dt', 'contact', 'contact_id',)
        read_only_fields = ('id',)



