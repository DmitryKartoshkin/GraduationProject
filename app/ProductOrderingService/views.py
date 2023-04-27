from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from django.http import JsonResponse

from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from requests import get

from rest_framework import filters


from yaml import load as load_yaml, Loader, safe_load


from ProductOrderingService.models import Shop, Category, Product, ProductInfo, Parameter, ProductParameter
from ProductOrderingService.serializers import ShopSerializer, ProductSerializer



class UploadViewSet(APIView):
    def post(self, request, *args, **kwargs):
        # if not request.user.is_authenticated:
        #     return JsonResponse({'Status': False, 'Error': 'Log in required'}, status=403)

        # if request.user.type != 'shop':
        #     return JsonResponse({'Status': False, 'Error': 'Только для магазинов'}, status=403)
        #
        # url = request.data.get('url')
        #
        # if url:
        #     validate_url = URLValidator()
        #     try:
        #         validate_url(url)
        #     except ValidationError as e:
        #         return JsonResponse({'Status': False, 'Error': str(e)})
        #     else:
        #         stream = get(url).content
        with open('shop1.yaml', encoding='UTF-8') as f:
            data = load_yaml(stream=f, Loader=Loader)

            shop, v = Shop.objects.get_or_create(name=data['shop'], user_id=request.user.id)
            for category in data['categories']:
                category_object, v = Category.objects.get_or_create(id=category['id'], name=category['name'])
                category_object.shops.add(shop.id)
                category_object.save()
                # ProductInfo.objects.filter(shop_id=shop.id).delete()
            for item in data['goods']:
                product, v = Product.objects.get_or_create(name=item['name'], category_id=item['category'])

                product_info = ProductInfo.objects.create(product_id=product.id,
                                                          external_id=item['id'],
                                                          model=item['model'],
                                                          price=item['price'],
                                                          price_rrc=item['price_rrc'],
                                                          quantity=item['quantity'],
                                                          shop_id=shop.id)
                for name, value in item['parameters'].items():
                    parameter_object, v = Parameter.objects.get_or_create(name=name)
                    ProductParameter.objects.create(product_info_id=product_info.id,
                                                    parameter_id=parameter_object.id,
                                                    value=value)

            return JsonResponse({'Status': True})
            #
            # return JsonResponse({'Status': False, 'Errors': 'Не указаны все необходимые аргументы'})


class ProductViewSet(APIView):
    def get(self, request):

        queryset = Product.objects.all().values()
        for q in queryset:
            print(type(q))
        print(queryset)
        return JsonResponse({'Products': list(queryset)})



# class ProductViewSet(ModelViewSet):
#     queryset = Product.objects.all()
#     serializer_class = ProductSerializer
#
#     def list(self, request):
#         print(dir(self.queryset))
#         return JsonResponse({'Status': "ok"})


