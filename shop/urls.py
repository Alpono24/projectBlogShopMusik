from django.urls import path, include
from .views import products_view, product_detail, cart_view, add_to_cart, remove_from_cart, delete_selected_products, \
    create_order, send_email_sell, order_is_sent, checkout_success, mark_items_as_selected, \
    pre_order, pre_order_confirmation, error_confirm_order, handler404, handler500

app_name = 'products'

urlpatterns = [
    path('', products_view, name='products'),

    path('product/<int:pk>/', product_detail, name='product_detail'),

    path('products_cart/', cart_view, name='cart_view'),
    path('products_cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),

    path('delete_selected/', delete_selected_products, name='delete_selected'),   # Новый путь для массового удаления

    path('products_cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('products/mark_items_as_selected/', mark_items_as_selected, name='mark_items_as_selected'),
    path('products/pre_order/', pre_order, name='pre_order'),
    path('products/pre_order_confirmation/', pre_order_confirmation, name='pre_order_confirmation'),

    path('products/create_order/', create_order, name='create_order'),

    path('products/send_email_sell/<int:order_id>/', send_email_sell, name='send_email_sell'),


    path('products/order_is_sent/', order_is_sent, name='order_is_sent'),
    path('products/checkout_success/', checkout_success, name='checkout_success'),
    path('products/error_confirm_order/', error_confirm_order, name='error_confirm_order'),


]
