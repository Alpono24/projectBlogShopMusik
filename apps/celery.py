import os  # Подключаем модуль операционной системы для взаимодействия с переменными окружения
from celery import Celery  # Импортируем класс Celery для инициализации Celery-приложения

from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'apps.settings') # Устанавливаем окружение DJANGO_SETTINGS_MODULE для загрузки настроек Django

app = Celery('apps') # Создаем экземпляр Celery с названием вашего проекта
app.config_from_object('django.conf:settings', namespace='CELERY') # Загружаем настройки Celery из settings.py
app.autodiscover_tasks() # Автоматически находим и регистрируем задачи Celery в проекте (Celery сам найдет все файлы с tasks.py / не нужно делать ручных импортов)



# Celery Beat schedule
# app.conf.beat_schedule = {
#     'add-every-30-seconds':
#         { 'task': 'myapp.tasks.add',
#           'schedule': 30.0, #30 секунд
#           'args': (16, 16),
#           },
#     'run-every-midnight': {
#         'task': 'myapp.tasks.scheduled_task',
#         # 'schedule': crontab(hour=0, minute=0),
#         'schedule': 10.0,
#     },
# }
#
#
#
