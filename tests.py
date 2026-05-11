from django.test import TestCase

# Create your tests here.
import psycopg2
from psycopg2 import OperationalError

# ЗАМЕНИТЕ ЭТИ ДАННЫЕ НА ВАШИ РЕАЛЬНЫЕ (из .env файла)
# Скорее всего, их нужно будет только скопировать из настроек.
conn_params = {
    "dbname": "postgres",      # На время проверки можно подключиться к стандартной БД "postgres"
    "user": "postgres",
    "password": "123",  # <--- ВАШ ПАРОЛЬ
    "host": "localhost",
    "port": "5432"
}

try:
    with psycopg2.connect(**conn_params) as conn:
        print("✅ Подключение успешно!")
except OperationalError as e:
    # Пробуем декодировать сообщение об ошибке в кодировку Windows-1251
    try:
        # e.args[0] - это байтовая строка с сообщением от сервера
        real_error_message = e.args[0].decode('windows-1251')
        print(f"🔴 Реальная ошибка подключения: {real_error_message}")
    except:
        # Если декодирование не удалось, выводим сырую ошибку
        print(f"🔴 Ошибка подключения (не удалось декодировать): {e}")