
from celery import shared_task  # Импортируем декоратор shared_task для создания фоновых задач в Celery
from decimal import Decimal # Импортируем класс Decimal
import requests  # Стандартная библиотека Python для отправки HTTP-запросов
from shop.models import Product  # Импортируем модель Product из нашего приложения shop

from celery.schedules import crontab # Импортируется класс crontab для настройки расписания задач по типу cron
from celery import current_app # Загружается ссылка на текущий экземпляр Celery-приложения, позволяющий получать доступ к общим настройкам и объектам приложения


@shared_task # Объявляем функцию update_prices_byn как асинхронную задачу Celery
def update_prices_byn():
    """
    Задача для автоматической конвертации цен на сайте из долларов США в белорусские рубли на основе курса нацбанка РБ.
    Выполняется каждый час.
    """
    try:
        # Обращаемся к API Нацбанка РБ для получения текущего курса доллара
        url = 'https://www.nbrb.by/api/exrates/rates/431' # URL API для получения курса доллара США
        response = requests.get(url) # Отправляем GET-запрос на указанный URL
        if response.status_code != 200:  # Проверяем статус ответа
            print(f"Статус ответа: {response.status_code}, Ответ: {response.text}")
            raise Exception("Ошибка получения курса валюты.")

        data = response.json() # Парсим JSON-данные из ответа
        print(data)  # Вывод полного ответа для анализа структуры

        official_rate = Decimal(str(data["Cur_OfficialRate"]))  # Извлекаем текущий курс доллара к белорусскому рублю и Преобразуем курс доллара в Decimal
        print(f"Полученный курс доллара: {official_rate}")

        for product in Product.objects.all():
            if product.price is not None:
                # Пересчитываем цену в долларах с округлением до двух знаков после запятой
                price_in_byn = round(product.price * official_rate, 2)
                product.price_in_byn = price_in_byn
                product.save()  # Сохраняем изменения в базу данных

    except Exception as e:
        print(f"Ошибка обновления цен: {e}")

# Регистрация расписания запуска задачи каждую минуту
# current_app.add_periodic_task(crontab(), update_prices.s())  # Регистрируем задачу, которая выполняется каждую минуту

# Регистрация расписания запуска задачи КАЖДЫЙ ЧАС
current_app.add_periodic_task(crontab(minute=0, hour='*'), update_prices_byn.s())  # Регистрируем задачу, которая выполняется каждый час ровно в 0 минут


@shared_task
def update_prices_eur():
    """
    Задача для автоматического обновления цен на сайте в евро на основе информации из базы данных.
    Конвертация происходит после того как появится информация о курсе доллара к белорусскому рублю.
    Выполняется каждый час.
    """
    try:
        url = 'https://www.nbrb.by/api/exrates/rates/451' # URL API для получения курса EUR
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Статус ответа: {response.status_code}, Ответ: {response.text}")
            raise Exception("Ошибка получения курса валюты.")
        data = response.json()
        print(data)
        official_rate = Decimal(str(data["Cur_OfficialRate"]))
        print(f"Полученный курс евро: {official_rate}")

        for product in Product.objects.all():
            if product.price is not None:
                price_in_eur = round(product.price_in_byn / official_rate, 2)
                product.price_in_eur = price_in_eur
                product.save()

    except Exception as e:
        print(f"Ошибка обновления цен: {e}")

current_app.add_periodic_task(crontab(minute=0, hour='*'), update_prices_eur.s())