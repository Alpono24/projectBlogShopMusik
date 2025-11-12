from django.urls import path
from .views import test_api

from .views import test_api, ProductDetailAPIView, ProductListAPIView, ProductCreateAPIView, set_cookie_example, get_cookie_example

app_name = 'shop_api'


urlpatterns = [
    path('test/<int:pk>/', test_api, name='test'),

    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),

    path('set-cookie/', set_cookie_example),
    path('get-cookie/', get_cookie_example),
]