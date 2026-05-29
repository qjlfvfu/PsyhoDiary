import os
import sys
import django
from django.db import connection
from django.contrib.auth import get_user_model

# Устанавливаем переменные окружения для теста
os.environ["DB_HOST"] = "localhost"
os.environ["DJANGO_SETTINGS_MODULE"] = "config.settings"

# Добавляем путь к проекту
sys.path.append(os.path.dirname(__file__))

django.setup()


User = get_user_model()


def test_database():
    print("\n" + "=" * 50)
    print("ТЕСТ ПОДКЛЮЧЕНИЯ К БАЗЕ ДАННЫХ")
    print("=" * 50 + "\n")

    # Тест 1: Подключение к БД
    try:
        connection.ensure_connection()
        print("✅ [1/3] Подключение к базе данных - УСПЕШНО")
    except Exception as e:
        print(f"❌ [1/3] Ошибка подключения: {e}")
        return False

    # Тест 2: Версия PostgreSQL
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version()")
            version = cursor.fetchone()[0].split(",")[0]
            print(f"✅ [2/3] PostgreSQL версия - {version}")
    except Exception as e:
        print(f"❌ [2/3] Ошибка: {e}")
        return False

    # Тест 3: Имя базы данных
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_database()")
            db_name = cursor.fetchone()[0]
            print(f"✅ [3/3] База данных - {db_name}")
    except Exception as e:
        print(f"❌ [3/3] Ошибка: {e}")
        return False

    print("\n" + "=" * 50)
    print("✅ ВСЕ ТЕСТЫ ПРОЙДЕНЫ")
    print("=" * 50)
    return True


if __name__ == "__main__":
    test_database()
