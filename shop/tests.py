from decimal import Decimal
from http.client import responses

from django.test import TestCase
from rest_framework import status, response
from rest_framework.test import APITestCase

# Create your tests here.

from .models import Product, Category


# #1 Unit test #1
class ProductTests(TestCase):
    def test_price_with_vat(self):
        product = Product(name = 'Smartphone', price = Decimal('1000.00'))
        self.assertEqual(product.price_with_vat, Decimal('1200'))
    def test_apply_discount(self):
          product = Product(name='Smartphone', price=Decimal('500.00'))
          discounted = product.apply_discount(10)
          self.assertEqual(discounted, 450.00)



# #2 Integration test #2
class ProductIntegrationTests(APITestCase):
    # тест с положительной ценой №1
    def test_create_product(self):
        data ={'name': 'Laptop', 'price': '1000.0'}
        response = self.client.post('/shop_api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='Laptop').exists())

    # тест с отрицательной ценой №2
    def test_create_product_price_incorrect(self):
        data ={'name': 'Laptop', 'price': '-1000.0'}
        response = self.client.post('/shop_api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


#3 Functional test #3
class ProductListTests(APITestCase):
    def test_get_products(self):
        Product.objects.create(name = 'Samsung', price = '999.99')
        response = self.client.get('/shop_api/products/')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Samsung', str(response.data))

#4 Performance Testing (Нагрузочное тестирование) - выдержит ли система нагрузку №4
#5 Регрессионное тестирование - старые функции остались рабочими после новых фич. Не сломалось ли что-то после измененийй в коде №5
#6 UI Testing - все ли отображается и все ли щёлкается ... кроме кода. Проверяем интерфейс №6
#7 Compatibility Testing - функционирование и взаимодействие с различными окружениями №7
#8 Acceptance Testing (Приемочное тестирование) После этого тестирования продукт считается готовым №8


# Test CRUD operations

class ProductModelTest(TestCase):
    def test_crud_operations(self):
        product = Product.objects.create(name = 'Tablet', price = '1000')
        self.assertEqual(Product.objects.count(), 1)

        product.price =900
        product.save()
        self.assertEqual(Product.objects.get(pk = product.pk).price, 900)

        product.delete()
        self.assertEqual(Product.objects.count(), 0)


class ProductViewTests(TestCase):
    def test_product_detail_found(self):
            product = Product.objects.create(name = 'Mac Book', price = 100)
            response = self.client.get(f'/shop_api/products/{product.id}/')
            self.assertEqual(response.status_code, 200)
            self.assertIn('Mac Book', response.json()['name'])


    # def test_redirect_after_register(self):
    #         response = self.client.post('/register/',{
    #            'username': 'user',
    #            'password': '123',
    #            'password2': '123',
    #            'email': 'test@example.com'
    #         })
    #         self.assertEqual(response.status_code, 302)
    #         self.assertIn('/', response['Location'])

# 3 Strategy
# Black Box Test Strategy
class ProductBlackBoxTests(APITestCase):
    def test_create_product(self):
        data ={'name': 'Laptop', 'price': '1000.0'}
        response = self.client.post('/shop_api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


# White Box Test Strategy
class ProductWhiteBoxTests(APITestCase):
    def test_price_with_vat_calculation(self):
        product = Product(name='Smartphone', price=Decimal('1000.00'))
        result = product.price_with_vat
        self.assertEqual(result, Decimal('1200'))

# Grey Box Test Strategy







# class ProductModelTest(TestCase):
#     @classmethod
#     def setUpTestData(cls):
#         # Создаем категорию для привязки продукта
#         cls.category = Category.objects.create(name="Electronics")
#
#         # Создаем продукт
#         cls.product = Product.objects.create(
#             name="Smartphone",
#             description="A high-quality smartphone with advanced features.",
#             price=999.99,
#             in_stock=True,
#             category=cls.category
#         )
#
#     def test_product_name_label(self):
#         field_label = self.product._meta.get_field('name').verbose_name
#         self.assertEqual(field_label, 'name')
#
#     def test_description_blank(self):
#         """Проверяем, что поле описания может быть пустым"""
#         product = Product.objects.get(id=self.product.id)
#         empty_instance = Product(name="Empty Product", price=0.00)
#         self.assertTrue(product.description == "" or empty_instance.description == "")
#
#     def test_price_max_digits_and_decimal_places(self):
#         max_digits = self.product._meta.get_field('price').max_digits
#         decimal_places = self.product._meta.get_field('price').decimal_places
#         self.assertEqual(max_digits, 10)
#         self.assertEqual(decimal_places, 2)
#
#     def test_in_stock_default_value(self):
#         """Тестируем значение поля по умолчанию"""
#         product = Product.objects.get(id=self.product.id)
#         self.assertTrue(product.in_stock)
#
#     def test_category_relation(self):
#         """Проверяем связь продукта с категорией"""
#         self.assertIsNotNone(self.product.category)
#         self.assertEqual(str(self.product.category), "Electronics")
#
#     def test_image_field_nullable(self):
#         """Тестируем nullable поле изображения"""
#         product_without_image = Product.objects.create(
#             name="No Image Product",
#             price=100.00,
#             in_stock=False
#         )
#         self.assertFalse(product_without_image.image)