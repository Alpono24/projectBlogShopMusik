from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import register_view
# from .apps.shop_api.views import RegisterAPIView, LogoutAPIView # не настроен путь импорта!!!!!!!!!!!!! поэтому оставил это сразу во вьюхах шоп_айпи

app_name = 'registration'

urlpatterns = [

path('register/', register_view, name='register'),
path('login/', LoginView.as_view(template_name='login.html'), name='login'),
path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

# path('register/', RegisterAPIView.as_view(), name='api_register'),  # не настроен путь импорта!!!!!!!!!!!!! поэтому оставил это сразу во вьюхах шоп_айпи

# path('logout/', LogoutAPIView.as_view(), name='api_logout'),  # опц: отзыв refresh # не настроен путь импорта!!!!!!!!!!!!! поэтому оставил это сразу во вьюхах шоп_айпи
]

