  # Базовый образ Python
  FROM python:3.11-buster




  # Рабочая директория
  WORKDIR /code

  # Копируем требования
  COPY requirements.txt .

  # Установка зависимостей
  RUN pip install -r requirements.txt

  # Копируем остальной код
  COPY . .

  # Запуск Django с помощью Gunicorn
  CMD ["gunicorn", "apps.wsgi:application", "--bind", "0.0.0.0:8000"]


