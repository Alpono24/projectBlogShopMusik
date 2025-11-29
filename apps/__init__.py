from .celery import app as celery_app
__all__ = ('celery_app',) # типовая настройка, для запуска Celery совместно с Django