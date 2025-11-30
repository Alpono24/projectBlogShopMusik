from django.core.validators import MinValueValidator
from django.db import models
from decimal import Decimal


class Product(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    price_in_byn = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    price_in_eur = models.DecimalField(max_digits=10, decimal_places=2, default=None, null=True, blank=True)
    in_stock = models.BooleanField(default=True)
    category = models.ForeignKey(
        'Category',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    image = models.ImageField(upload_to='shop/product_images/', blank=True, null=True)

    @property
    def price_with_vat(self):
        return self.price * Decimal('1.20')

    def apply_discount(self, percent):
        return float(self.price) * (1 - percent / 100)

    def save(self, *args, **kwargs):
        """
        Переопределение метода save().
        Проверяем, новый ли товар и отправляем письмо, если да.
        """
        is_new = not self.pk  # True, если pk отсутствует (новый товар)
        super().save(*args, **kwargs)  # Сохраняем изменения в БД

        if is_new:
            from .tasks import emails_new_product
            emails_new_product.delay(self.id, self.name)  # Асинхронная отправка уведомления



class Category(models.Model):
    objects = models.Manager()

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name





