from celery import shared_task
from decimal import Decimal
import requests
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import CurrencyRateUSD, CurrencyRateEUR, CartItem, Order
from celery.schedules import crontab
from celery import current_app
from django.core.mail import send_mail
from django.contrib.auth.models import User
import logging
from pathlib import Path

# Запуск планировщика Celery Beat и рабочего процесса Celery Worker в отдельных окнах терминала:
# 1. Запуск планировщика Celery Beat: celery -A apps beat -l info
# 2. Запуск рабочего процесса Celery Worker: celery -A apps worker -l info

BASE_DIR = Path(__file__).resolve().parent.parent

LOG_DIR = BASE_DIR / 'shop' / 'log_file'

if not LOG_DIR.exists():
    LOG_DIR.mkdir(parents=True)

MAIL_LOG_PATH = LOG_DIR / 'log_send_mail.log'
PRICE_LOG_PATH = LOG_DIR / 'log_update_course_BYN_USD_EUR.log'
CART_LOG_PATH = LOG_DIR / 'log_send_mail_admin_and_customer.log'

mail_logger = logging.getLogger('mail')
mail_logger.setLevel(logging.DEBUG)
mail_handler = logging.FileHandler(MAIL_LOG_PATH)
mail_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
mail_logger.addHandler(mail_handler)

price_logger = logging.getLogger('prices')
price_logger.setLevel(logging.DEBUG)
price_handler = logging.FileHandler(PRICE_LOG_PATH)
price_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
price_logger.addHandler(price_handler)

cart_logger = logging.getLogger('cart')
cart_logger.setLevel(logging.DEBUG)
cart_handler = logging.FileHandler(CART_LOG_PATH)
cart_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
cart_logger.addHandler(cart_handler)



@shared_task #
def update_currency_rate_usd_nbrb():
    """
    Задача для автоматической конвертации долларов США в белорусские рубли на основе курса нацбанка РБ.
    Выполняется каждый час.
    """
    print("Старт обновления курса валюты update_currency_rate_usd_nbrb!")
    price_logger.info(f"Старт обновления курса валюты update_currency_rate_usd_nbrb!")

    try:
        url = 'https://www.nbrb.by/api/exrates/rates/431'
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Статус ответа: {response.status_code}, Ответ: {response.text}")
            price_logger.error(f"Статус ответа: {response.status_code}, Ответ: {response.text}")
            raise Exception("Ошибка получения курса валюты.")

        data = response.json()

        print(f"Успешно:JSON ответ по курсу USD: {data}")
        price_logger.info(f"Успешно:JSON ответ по курсу USD: {data}")

        official_rate = Decimal(str(data["Cur_OfficialRate"]))

        print(f"Полученный курс BYN/USD: {official_rate}")
        price_logger.info(f"Полученный курс BYN/USD: {official_rate}")

        # obj, created = CurrencyRateUSD.objects.update_or_create(currency_usd='BYN/USD', defaults={'rate_usd': official_rate})
        new_entry = CurrencyRateUSD(currency_usd='BYN/USD', rate_usd=official_rate)
        new_entry.save()

    except Exception as e:
        print(f"Ошибка обновления курса BYN/USD: {e} ")
        price_logger.error(f"Ошибка обновления курса BYN/USD: {e} ")

current_app.add_periodic_task(crontab(minute='0', hour='*'), update_currency_rate_usd_nbrb.s())



@shared_task #
def update_currency_rate_eur_nbrb():
    """
    Задача для автоматической конвертации долларов США в евро на основе курса нацбанка РБ.
    Выполняется каждый час.
    """
    print("Старт обновления курса валюты update_currency_rate_eur_nbrb!")
    price_logger.info(f"Старт обновления курса валюты update_currency_rate_eur_nbrb!")

    try:
        url = 'https://www.nbrb.by/api/exrates/rates/451'
        response = requests.get(url)

        if response.status_code != 200:
            print(f"Статус ответа: {response.status_code}, Ответ: {response.text}")
            price_logger.error(f"Статус ответа: {response.status_code}, Ответ: {response.text}")
            raise Exception ("Ошибка получения курса валюты.")

        data = response.json()
        print(f"Успешно:JSON ответ по курсу EUR: {data}")
        price_logger.info(f"Успешно:JSON ответ по курсу EUR: {data}")

        official_rate = Decimal(str(data["Cur_OfficialRate"]))

        print(f"Полученный курс BYN/EUR: {official_rate}")
        price_logger.info(f"Полученный курс BYN/EUR: {official_rate}")

        # obj, created = CurrencyRateEUR.objects.update_or_create(currency_eur='BYN/EUR', defaults={'rate_eur': official_rate})
        new_entry = CurrencyRateEUR(currency_eur='BYN/EUR', rate_eur=official_rate)
        new_entry.save()

    except Exception as e:
        print(f"Ошибка обновления BYN/EUR: {e} ")
        price_logger.error(f"Ошибка обновления BYN/EUR: {e} ")

current_app.add_periodic_task(crontab(minute='0', hour='*'), update_currency_rate_eur_nbrb.s())



@shared_task
def emails_new_product(product_id, product_name):
    """
    Задача для отправки уведомления на почту пользователей о новом товаре.
    Письма отправляются на почту зарегистрированных пользователей.
    """
    print(f"Старт отправки письма о новом продукте:  {product_name}")
    mail_logger.info(f"Старт отправки письма о новом продукте:  {product_name}")

    subject = f'Новый товар в нашем магазине: {product_name}'
    message = f"""
    Уважаемый покупатель!
    Мы рады представить Вам новый продукт: {product_name}.
    Посмотрите подробности на сайте нашего магазина https://alpono24.pythonanywhere.com/products/product/{product_id}/
    Спасибо за внимание!
    """
    from_email = 'alex.ponomarov@mail.ru'
    emails = list(User.objects.values_list('email', flat=True))

    try:
        result = send_mail(subject, message, from_email, emails)
        print(f"Письмо о добавлении нового продукта {product_name} ({result}) успешно отправлено для: {emails}")
        mail_logger.info(f"Письмо о добавлении нового продукта {product_name} ({result}) успешно отправлено для: {emails}")
    except Exception as e:
        print(f"Ошибка при отправке письма: {e} о добавлении нового продукта {product_name}")
        mail_logger.info(f"Ошибка при отправке письма: {e} о добавлении нового продукта {product_name}")



@shared_task
def send_admin_new_order_email(order_id):
    """
    Задача Celery для отправки письма админу сайта о поступлении заказа
    """
    try:
        order = Order.objects.get(pk=order_id)
        rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
        rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()

        subject = f'Новый заказ №{order.pk}'
        context = {
            'order': order,
            'user': order.user,
            'rate_usd': rate_usd,
            'rate_eur': rate_eur,
        }
        html_message = render_to_string('new_order_admin.html', context)
        plain_message = strip_tags(html_message)

        recipient_list = ['alex.ponomarov@mail.ru']

        send_mail(subject, plain_message, None, recipient_list, html_message=html_message)

        print(f"Письмо продавцу по заказу {order_id} отправлено успешно!")
        cart_logger.info(f"Письмо продавцу по заказу {order_id} отправлено успешно!")
    except Exception as e:
        print(f"Ошибка отправки письма продавцу: {e} по заказу {order_id}")
        cart_logger.info(f"Ошибка отправки письма продавцу: {e} по заказу {order_id}")



@shared_task
def send_customer_email(order_id):
    """
    Задача Celery для отправки письма покупателю о принятии админом магазина заказа
    """
    try:
        order = Order.objects.get(pk=order_id)
        rate_usd = CurrencyRateUSD.objects.order_by('-created_at').first()
        rate_eur = CurrencyRateEUR.objects.order_by('-created_at').first()
        subject = f'Ваш заказ №{order.pk} принят!'
        context = {
            'order': order,
            'user': order.user,
            'rate_usd': rate_usd,
            'rate_eur': rate_eur,
        }
        html_message = render_to_string('confirm_order.html', context)
        plain_message = strip_tags(html_message)

        recipient_list = [order.user.email]

        send_mail(subject, plain_message, None, recipient_list, html_message=html_message)

        print(f"Письмо покупателю по заказу {order_id} отправлено успешно!")
        cart_logger.info(f"Письмо покупателю по заказу {order_id} отправлено успешно!")
    except Exception as e:
        print(f"Ошибка отправки письма покупателю: {e} по заказу {order_id}")
        cart_logger.info(f"Ошибка отправки письма покупателю: {e} по заказу {order_id}")



@shared_task
def clean_cart(user_id, order_id):
    """
    Задача Celery для очистки корзины после успешного оформления заказа.
    """
    # cart_logger.info(f"Приступаем к очистке корзины по заказу: {order_id}")
    cart_items = CartItem.objects.filter(user_id=user_id, selected=True)
    cart_items.delete()
    cart_logger.info(f"Корзина очищена для заказа {order_id}")





































