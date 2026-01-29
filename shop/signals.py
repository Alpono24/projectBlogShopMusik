from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Product
from .tasks import emails_new_product

@receiver(post_save, sender=Product)
def send_notification(sender, instance, created, **kwargs):
    """
    Функция обработки сигнала post_save.
    Отправляет уведомление о создании нового товара.
    """
    if created:
        emails_new_product.delay(instance.id, instance.name)


@receiver(post_save, sender=Product)
def update_in_stock(sender, instance, **kwargs):
    """
    Автоматически устанавливает статус доступности товара исходя из количества
    """
    if instance.quantity > 0:
        instance.in_stock = True
    else:
        instance.in_stock = False

    if kwargs['update_fields'] is None or 'in_stock' not in kwargs['update_fields']:
        instance.save(update_fields=['in_stock'])