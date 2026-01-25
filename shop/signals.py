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
    """Автоматически меняет доступность товара при изменении количества."""
    old_instance = Product.objects.get(pk=instance.pk)
    if old_instance.quantity == 0 and instance.quantity > 0:
        instance.in_stock = True
    elif old_instance.quantity > 0 and instance.quantity == 0:
        instance.in_stock = False

    if old_instance.in_stock != instance.in_stock:
        instance.save(update_fields=['in_stock'])
