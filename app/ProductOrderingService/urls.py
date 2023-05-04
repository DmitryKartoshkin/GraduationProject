from rest_framework.routers import DefaultRouter, SimpleRouter
from django.urls import path, include
from ProductOrderingService.views import *
# UploadViewSet, ProductView, CategoryView, ProductInfoView

app_name = 'ProductOrderingService'
router = DefaultRouter()
# router = SimpleRouter()
router.register(r'products', ProductViewSet)
router.register(r'orders', OrderViewSet)
# router.register(r'user', UserViewSet)
# router.register(r'user', RegistrUserView)

urlpatterns = [
    path('update/', UploadViewSet.as_view(), name='update'),
    path('', include(router.urls)),
    path('registr/', RegistrUserView.as_view(), name='registr'),

]


