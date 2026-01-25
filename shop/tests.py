from decimal import Decimal
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase
from .models import Product



class ProductTests(TestCase):
    def test_price_with_vat(self):
        product = Product(name = 'Smartphone', price = Decimal('1000.00'))
        self.assertEqual(product.price_with_vat, Decimal('1200'))
    def test_apply_discount(self):
          product = Product(name='Smartphone', price=Decimal('500.00'))
          discounted = product.apply_discount(10)
          self.assertEqual(discounted, 450.00)



class ProductIntegrationTests(APITestCase):

    def test_create_product(self):
        data ={'name': 'Laptop', 'price': '1000.0'}
        response = self.client.post('/shop_api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Product.objects.filter(name='Laptop').exists())



    def test_create_product_price_incorrect(self):
        data ={'name': 'Laptop', 'price': '-1000.0'}
        response = self.client.post('/shop_api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



class ProductListTests(APITestCase):
    def test_get_products(self):
        Product.objects.create(name = 'Samsung', price = '999.99')
        response = self.client.get('/shop_api/products/')
        print(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Samsung', str(response.data))



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



class ProductBlackBoxTests(APITestCase):
    def test_create_product(self):
        data ={'name': 'Laptop', 'price': '1000.0'}
        response = self.client.post('/shop_api/products/create/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class ProductWhiteBoxTests(APITestCase):
    def test_price_with_vat_calculation(self):
        product = Product(name='Smartphone', price=Decimal('1000.00'))
        result = product.price_with_vat
        self.assertEqual(result, Decimal('1200'))





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