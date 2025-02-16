# Используем официальный базовый образ PostgreSQL (15-я версия, можно менять при необходимости)
FROM postgres:15

# Устанавливаем переменные окружения для PostgreSQL:
ENV POSTGRES_USER=demo_user
ENV POSTGRES_PASSWORD=demo_pass
ENV POSTGRES_DB=demo_db

RUN apt-get update && apt-get install -y --no-install-recommends nano

EXPOSE 5432

