# Используйте официальный образ Python как базовый
FROM python:3.10

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте файлы проекта в контейнер
COPY . /app

# Установите зависимости
RUN pip install -r requirements.txt


# Команда для запуска Daphne
CMD python3 -m daphne -p 8666 -b 0.0.0.0 webProject.asgi:application
