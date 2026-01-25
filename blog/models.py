from django.db import models
from django.conf import settings

from datetime import datetime
now = datetime.now()
formatted_date_time = now.strftime("%d.%m.%y %H:%M")



class Post(models.Model):
    title = models.CharField(max_length=100, blank=False, verbose_name="Заголовок")
    body = models.TextField(blank=False, verbose_name="Статья")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Автор")
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    image = models.ImageField(upload_to='blog/post_images/', blank=True, null=True, verbose_name="Изображение")

    class Meta:
        verbose_name = '1. Статья'
        verbose_name_plural = '1. Статьи'



class Category(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '2. Категория'
        verbose_name_plural ='2. Категории'



