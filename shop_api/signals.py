from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.cache import cache
from shop.models import Product
import logging


logger = logging.getLogger(__name__)

@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, created, **kwargs):
    logger.info(f"Cleaning cache on save of product {instance.pk}.")
    cache.delete('all_products')