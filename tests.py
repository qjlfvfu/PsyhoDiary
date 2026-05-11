# Create your tests here.
import psycopg2
from psycopg2 import OperationalError

conn_params = {
    "dbname": "my_diary",
    "user": "postgres",
    "password": "123",
    "host": "localhost",
    "port": "5432",
}

try:
    with psycopg2.connect(**conn_params) as conn:
        print("✅ Подключение успешно!")
except OperationalError as e:
    print(f"🔴 Ошибка подключения: {e}")
