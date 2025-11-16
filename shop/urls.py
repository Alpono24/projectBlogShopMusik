from django.urls import path
from .views import products_view, product_detail, cart_view, add_to_cart, remove_from_cart

app_name = 'products'

urlpatterns = [
    path('', products_view, name='products'),

    path('product/<int:pk>/', product_detail, name='product_detail'),


    path('products_cart/', cart_view, name='cart_view'),
    path('products_cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('products_cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
]
