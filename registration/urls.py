from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import register_view

app_name = 'registration'

urlpatterns = [

path('register/', register_view, name='register'),
path('login/', LoginView.as_view(template_name='login.html'), name='login'),
path('logout/', LogoutView.as_view(next_page='/'), name='logout'),

]

