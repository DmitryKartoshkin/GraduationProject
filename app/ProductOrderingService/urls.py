from rest_framework.routers import DefaultRouter
from django.urls import path
from ProductOrderingService.views import UploadViewSet, ProductView, CategoryView, ProductInfoView

app_name = 'ProductOrderingService'
# router = DefaultRouter()
#
# router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('update/', UploadViewSet.as_view(), name='update'),
    path('products/', ProductView.as_view(), name='products'),
    path('categorys/', CategoryView.as_view(), name='categorys'),
    path('productinfo/', ProductInfoView.as_view(), name='productinfo'),
]

# + router.urls
