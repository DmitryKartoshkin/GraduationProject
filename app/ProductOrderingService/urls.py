from rest_framework.routers import DefaultRouter
from django.urls import path, include
from ProductOrderingService import views


app_name = 'ProductOrderingService'
router = DefaultRouter()

router.register(r'products', views.ProductViewSet)  # список продуктов
# router.register(r'basket', BasketViewSet)
router.register(r'shop',  views.ShopViewSet)  # список магазинов
router.register(r'category',  views.CategoriesViewSet)  # список категорий
router.register(r'order',  views.OrderViewSet)  # связки заказа и контакта
router.register(r'contacts',  views.ContactViewSet)


urlpatterns = [
    path('', include(router.urls)),
    # адрес для загрузка данных о продуктах из файла
    path('update/',  views.UploadViewSet.as_view(), name='update'),
    # адреса для работы пользователей с корзиной
    path('basket_order/',  views.BasketView.as_view(), name='basket_order'),
    path('basket_order/<int:pk>/',  views.BasketViewDetail.as_view(), name='basket_order_one'),
    # адреса для работы магазинов со статусом заказа
    path('shop_state/',  views.PartnerOrders.as_view(), name='shop_state'),

]


