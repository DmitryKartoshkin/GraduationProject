from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ProductOrderingService.views import *


app_name = 'ProductOrderingService'
router = DefaultRouter()

router.register(r'products', ProductViewSet)  # список продуктов
# router.register(r'basket', BasketViewSet)
router.register(r'shop', ShopViewSet)  # список магазинов
router.register(r'category', CategoriesViewSet)  # список категорий
router.register(r'order', OrderViewSet)  # связки заказа и контакта
router.register(r'contacts', ContactViewSet)

# router.register(r'test', TestViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # адрес для загрузка данных о продуктах из файла
    path('update/', UploadViewSet.as_view(), name='update'),
    # адреса для работы пользователей с корзиной
    path('basket_order/', BasketView.as_view(), name='basket_order'),
    path('basket_order/<int:pk>/', BasketViewDetail.as_view(), name='basket_order_one'),
    # адреса для работы магазинов со статусом заказа
    path('shop_state/', PartnerOrders.as_view(), name='shop_state'),


    # path('order/', OrderView.as_view(), name='order'),




    # path('registr/', RegistrUserView.as_view(), name='registr'),  # регистрация
]


