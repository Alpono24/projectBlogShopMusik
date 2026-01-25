from django.conf import settings
from django.core.validators import MinValueValidator, EmailValidator, RegexValidator
from django.db import models
from decimal import Decimal
from django.contrib.auth.models import User



class BrandName(models.Model):
    """
     Модель: Бренды и Производители
     """
    name = models.CharField(max_length=100, verbose_name="Название бренда")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '2. Бренды и Производители'
        verbose_name_plural = '2. Бренды и Производители'



class Unit(models.Model):
    """
    Модель: Единицы измерения
    """
    name = models.CharField(max_length=10, unique=True, verbose_name="Ед. изм.")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '4. Единица измерения'
        verbose_name_plural = '4. Единицы измерения'



class Product(models.Model):
    """
    Модель: Товары
    """
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Категория")
    seller = models.ForeignKey('Seller', on_delete=models.PROTECT, blank=True, null=True, verbose_name="Продавец")
    name = models.CharField(max_length=100, verbose_name="Наименование")
    brand = models.ForeignKey('BrandName', on_delete=models.PROTECT, blank=True, null=True,  verbose_name="Производитель")
    image = models.ImageField(upload_to='shop/product_images/', blank=True, null=True, verbose_name="Изображение")

    quantity = models.PositiveIntegerField(default=0, verbose_name="Количество на складе")

    unit = models.ForeignKey(Unit, on_delete=models.PROTECT, verbose_name="Ед. изм.", default=None)
    description = models.TextField(blank=True, verbose_name="Описание")

    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name="Цена в USD")
    price_in_byn = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True, blank=True, verbose_name="Цена в BYN")
    price_in_eur = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True, blank=True, verbose_name="Цена в EUR")

    in_stock = models.BooleanField(default=True, verbose_name="Наличие")
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name="Скидка (%)")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")


    @property
    def price_with_vat(self):
        return self.price * Decimal('1.20')


    def apply_discount(self, discount):
        return float(self.price) * (1 - discount / 100)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '1. Товар'
        verbose_name_plural = '1. Товары'



class Category(models.Model):
    """
    Модель: Категории товаров
    """
    name = models.CharField(max_length=100, verbose_name="Категория товара")
    icon_shop_category = models.ImageField(upload_to='shop_category_icons/', blank=True, null=True, verbose_name="Иконка категории")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '5. Категория товара'
        verbose_name_plural = '5. Категории товаров'




class CurrencyRateUSD(models.Model):
    """
    Модель: курс BYN/USD
    """
    rate_usd = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс")
    currency_usd = models.CharField(max_length=10, default='BYN/USD', verbose_name="Валюта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.currency_usd}: {self.rate_usd}"

    class Meta:
        verbose_name = '8. Курс BYN/USD НБРБ'
        verbose_name_plural ='8. Курс BYN/USD НБРБ'




class CurrencyRateEUR(models.Model):
    """
    Модель: курс BYN/EUR
    """
    rate_eur = models.DecimalField(max_digits=10, decimal_places=4, verbose_name="Курс")
    currency_eur = models.CharField(max_length=10, default='BYN/EUR', verbose_name="Валюта")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")

    def __str__(self):
        return f"{self.currency_eur}: {self.rate_eur}"

    class Meta:
        verbose_name = '9. Курс BYN/EUR НБРБ'
        verbose_name_plural ='9. Курс BYN/EUR НБРБ'



class CartItem(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    selected = models.BooleanField(default=False)

    def total_price(self):
        return self.product.price * self.quantity

    def unit_price(self):
        return self.product.price

    def get_total_cost(self):
        return self.total_price()

    def __str__(self):
        return f"{self.user.username}'s cart item: {self.product.name}"

    class Meta:
        verbose_name = '6. Корзина'
        verbose_name_plural ='6. Корзины'



class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="Пользователь")
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая сумма")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    notes = models.TextField(blank=True, null=True, verbose_name="Примечания")
    is_sent = models.BooleanField(default=False, verbose_name="Принято")
    STATUS_CHOICES = [
        ('pending', 'Ожидается оплата'),
        ('paid', 'Оплачено'),
        ('shipped', 'Отправлено'),
        ('delivered', 'Доставлено'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name="Статус заказа")

    def __str__(self):
        return f"Заказ №{self.pk}: {self.user.username}"

    class Meta:
        verbose_name = '7. Заказ'
        verbose_name_plural = '7. Заказы'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='details', on_delete=models.CASCADE, verbose_name="Заказ")
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name="Товар")
    quantity = models.PositiveIntegerField(default=1, verbose_name="Количество")

    def total_price(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f'{self.product.name} x {self.quantity}'

    class Meta:
        verbose_name = 'Деталь заказа'
        verbose_name_plural = 'Детали заказа'



class Seller(models.Model):
    """
    Модель: Продавцы
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='seller', verbose_name="Пользователь")
    company_name = models.CharField(max_length=100, verbose_name="Название компании")
    email = models.EmailField(validators=[EmailValidator(message="Некорректный e-mail.")],
                              verbose_name="Электронная почта")
    address = models.CharField(max_length=255, verbose_name="Адрес")

    phone_number = models.CharField(max_length=20,
                                    validators=[
                                        RegexValidator(r'^(\+\d{1,3}|\d)(\s|-|\.)?\d{3}(\s|-|\.)?\d{3}(\s|-|\.)?\d{4}$',
                                                       message="Номер телефона введен некорректно.")
                                    ], verbose_name="Телефон", )

    website = models.URLField(blank=True, verbose_name="Сайт")
    logo = models.ImageField(upload_to='shop/sellers_images/logos/', null=True, blank=True, verbose_name="Логотип")

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = '3. Продавец'
        verbose_name_plural = '3. Продавцы'



