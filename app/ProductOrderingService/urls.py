from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ProductOrderingService.views import *


app_name = 'ProductOrderingService'
router = DefaultRouter()

router.register(r'products', ProductViewSet)  # список продуктов
# router.register(r'basket', BasketViewSet)
router.register(r'shop', ShopViewSet)  # список магазинов
router.register(r'category', CategoriesViewSet)  # список категорий

urlpatterns = [
    path('', include(router.urls)),
    # адрес для загрузка данных о продуктах из файла
    path('update/', UploadViewSet.as_view(), name='update'),
    # адреса регистрации, активации и аутентификации с помощью Djoser
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('auth/', include('djoser.urls.jwt')),
    # адреса для работы пользователей с корзиной
    path('basket_order/', BasketView.as_view(), name='basket_order'),
    path('basket_order/<int:pk>/', BasketViewDetail.as_view(), name='basket_order_one'),
    # адреса для работы магазинов со статусом заказа
    path('shop_state/', PartnerOrders.as_view(), name='shop_state'),
    # адреса для работы с контактами
    path('contact/', ContactAllView.as_view(), name='contact'),
    path('contact/<int:pk>/', ContactView.as_view(), name='contact_one'),


    # path('registr/', RegistrUserView.as_view(), name='registr'),  # регистрация
]


