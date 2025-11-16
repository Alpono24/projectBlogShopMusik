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
