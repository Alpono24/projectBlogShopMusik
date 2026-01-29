import os
from celery import Celery  # Импортируем класс Celery для инициализации Celery-приложения

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings') # Устанавливаем окружение DJANGO_SETTINGS_MODULE для загрузки настроек Django

app = Celery('apps') # Создаем экземпляр Celery с названием вашего проекта
app.config_from_object('django.conf:settings', namespace='CELERY') # Загружаем настройки Celery из settings.py
app.autodiscover_tasks() # Автоматически находим и регистрируем задачи Celery в проекте (Celery сам найдет все файлы с tasks.py / не нужно делать ручных импортов)


