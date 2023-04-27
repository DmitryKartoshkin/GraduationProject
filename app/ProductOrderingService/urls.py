from rest_framework.routers import DefaultRouter
from django.urls import path
from ProductOrderingService.views import UploadViewSet, ProductViewSet

app_name = 'ProductOrderingService'
# router = DefaultRouter()
#
# router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    path('update/', UploadViewSet.as_view(), name='update'),
    path('products/', ProductViewSet.as_view(), name='products'),
]

# + router.urls
