
from django.urls import path
from .views import BlogListAPIView, PostDetailAPIView, PostCreateAPIView

app_name = 'blog_api'

urlpatterns = [
    # path('products/<int:pk>/', ProductDetailAPIView.as_view(), name='product-detail'),
    path('', BlogListAPIView.as_view(), name='blog-list'),
    path('post_detail/<int:pk>/', PostDetailAPIView.as_view(), name='post_detail'),
    path('post_create/', PostCreateAPIView.as_view(), name='post_create'),
]