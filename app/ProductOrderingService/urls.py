from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from ProductOrderingService.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
# UploadViewSet, ProductView, CategoryView, ProductInfoView

app_name = 'ProductOrderingService'
router = DefaultRouter()

router.register(r'products', ProductViewSet)  # список продуктов
router.register(r'orders', OrderViewSet)
router.register(r'shop', ShopViewSet)  # список магазинов
router.register(r'category', CategoriesViewSet)  # список категорий

urlpatterns = [
    path('update/', UploadViewSet.as_view(), name='update'),  # загрузка данных о продуктах из файла
    path('', include(router.urls)),
    path('registr/', RegistrUserView.as_view(), name='registr'),  # регистрация
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),  # аутентификация
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # продление действия токена.
    path('verify/', TokenVerifyView.as_view(), name='token_verify'),
    # path('products/', ProductView.as_view(), name='products'),  # продукты

]


