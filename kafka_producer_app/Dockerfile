# Используем Python 3.9
FROM python:3.9-slim

# Устанавливаем зависимости
RUN apt-get update && apt-get install -y \
    python3-pip && \
    rm -rf /var/lib/apt/lists/*

# Устанавливаем нужные библиотеки
RUN pip install confluent-kafka faker pandas

# Создаем рабочую директорию
WORKDIR /app

# Копируем код продюсера в контейнер
COPY producer.py /app/producer.py
# Копируем CSV файл с данными в контейнер
COPY superstore_data.csv /app/superstore_data.csv


# Указываем команду по умолчанию
CMD ["python", "/app/producer.py"]
