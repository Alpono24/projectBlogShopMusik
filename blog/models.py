from django.db import models
from django.conf import settings

from datetime import datetime
# Получаем текущую дату и время
now = datetime.now()
# Форматируем дату и время в нужный вид
formatted_date_time = now.strftime("%d.%m.%y %H:%M")
# print(formatted_date_time)


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=100, blank=False)
    body = models.TextField(blank=False)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='blog/post_images/', blank=True, null=True)


class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


