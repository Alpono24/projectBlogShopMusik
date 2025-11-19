from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APITestCase
from django.contrib.auth.models import User



# Create your tests here.


class SimpleJWTTest(APITestCase):
    def setUp(self):
        # Создаём обычного пользователя
        self.user = User.objects.create_user(username='user1', password='pass123')

    def test_can_access_protected_api(self):
        # Генерируем JWT токен для пользователя
        token = str(AccessToken.for_user(self.user))

        # Делаем GET-запрос к защищённому эндпоинту с токеном
        response = self.client.get(
            '/shop/products/',
            HTTP_AUTHORIZATION=f'Bearer {token}'
        )

        # Проверяем, что сервер не вернул 401 Unauthorized
        self.assertNotEqual(response.status_code, 401)




from django.core.cache import cache
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken
from shop.models import Product
from django.test import TestCase
#
class CacheTest(TestCase):
    def setUp(self):
        # Создаем фиктивный продукт
        Product.objects.create(name="Test Product", price=100)
        # Генерируем JWT-токен
        access_token = AccessToken.for_user(User.objects.create(username="testuser"))
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def test_cache_works_and_invalidation(self):
        # Отправляем запрос и проверяем успешность
        response = self.client.get(reverse('shop_api:product-list'))
        print(response.content.decode())  # Вывод содержимого ответа

        # Попытаемся считать кешированное значение
        old_cached_value = cache.get('all_products')
        print(f"Old cached value: {old_cached_value}")  # Просмотр старого кеша

        # Убедимся, что кеш сохранился после первого запроса
        assert old_cached_value is not None, "Кеш не создан после первого запроса"

        # Модифицируем продукт, чтобы изменить кеш
        product = Product.objects.first()
        product.price += 100
        product.save()

        # Еще раз запрашиваем данные и проверяем изменение
        new_response = self.client.get(reverse('shop_api:product-list'))
        print(new_response.content.decode())  # Вывод нового ответа

        # Убедимся, что кеш обновился
        new_cached_value = cache.get('all_products')
        print(f"New cached value: {new_cached_value}")  # Просмотр нового кеша

        # Проверим, что кеш действительно обновился
        assert old_cached_value != new_cached_value, "Кеш не обновился после изменения продукта"