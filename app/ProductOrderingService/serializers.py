from rest_framework.serializers import ModelSerializer, CharField, Serializer, EmailField, ValidationError

from ProductOrderingService.models import Shop, Product, Category, ProductInfo, Parameter, ProductParameter, User
#     Contact, Order, OrderItem


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = ('name', 'url', 'state')


class ProductInfoSerializer(ModelSerializer):
    class Meta:
        model = ProductInfo

        fields = ('model', 'quantity', 'price', 'price_rrc')


class ProductSerializer(ModelSerializer):
    product = ProductInfoSerializer(many=True)

    class Meta:
        model = Product
        fields = ('name',)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', )


class ParameterSerializer(ModelSerializer):
    class Meta:
        model = Parameter
        fields = ('name', )


class ProductParameterSerializer(ModelSerializer):
    class Meta:
        model = ProductParameter
        fields = ('value',)


# class ContactSerializer(ModelSerializer):
#     class Meta:
#         model = Contact
#         fields = ('city', 'street', 'house', 'structure', 'building', 'apartment', 'phone')
#
#
# class OrderSerializer(ModelSerializer):
#     class Meta:
#         model = Order
#         fields = ('state', 'contact')
#
#
# class OrderItemSerializer(ModelSerializer):
#     class Meta:
#         model = OrderItem
#         fields = ('quantity',)