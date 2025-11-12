from django.urls import path
from .views import music

app_name = 'music'

urlpatterns = [
    path('', music, name='music'),
]
