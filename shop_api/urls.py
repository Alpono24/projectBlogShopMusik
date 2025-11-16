from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .views import test_api, RegisterAPIView, LogoutAPIView

from .views import test_api, ProductDetailAPIView, ProductListAPIView, ProductCreateAPIView, set_cookie_example, get_cookie_example

app_name = 'shop_api'


urlpatterns = [
    path('test/<int:pk>/', test_api, name='test'),

    path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
    path('products/create/', ProductCreateAPIView.as_view(), name='product-create'),

    path('set-cookie/', set_cookie_example),
    path('get-cookie/', get_cookie_example),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('register/', RegisterAPIView.as_view(), name='api_register'),
    path('logout/', LogoutAPIView.as_view(), name='api_logout'),  # опц: отзыв refresh
]