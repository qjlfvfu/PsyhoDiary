# 🧠 PsyDiary — Психологический дневник

Веб-приложение для ведения личного дневника с отслеживанием настроения, мечтаний, привычек и приёма лекарств. Проект помогает пользователям анализировать своё психическое состояние, а врачам — отслеживать прогресс пациентов.

---

## 📋 Основные возможности

### 👤 Пользователи
- Регистрация и аутентификация (email + пароль)
- Роли: **Пациент**, **Врач**, **Модератор**
- Врачи могут вести список пациентов и получать оповещения

### 📓 Дневник
- Создание, редактирование, удаление записей
- Оценка настроения (от 1 до 5)
- Поиск по заголовку и содержимому
- Пагинация записей

### ✨ Мечты и цели
- Добавление, редактирование, удаление
- Статусы: черновик, в процессе, исполнено, отложено

### 🔄 Трекер привычек
- Создание привычек с периодичностью
- Отметка выполнения (с логированием)

### 💊 Трекер таблеток
- Добавление лекарств (дозировка, время приёма, дни)
- Отметка приёма

### 🧠 Психологические тесты
- Прохождение тестов (опросники)
- Сохранение результатов

### 🆘 Экстренная помощь
- Контакты служб поддержки
- Круглосуточные телефоны доверия

---

## 🛠️ Технологии

| Компонент | Технология |
|-----------|-----------|
| **Backend** | Django 6.0.5 |
| **API** | Django REST Framework |
| **База данных** | PostgreSQL 15 |
| **Кэш и брокер** | Redis |
| **Фоновые задачи** | Celery + Celery Beat |
| **Контейнеризация** | Docker + Docker Compose |
| **Веб-сервер** | Gunicorn + Nginx |
| **Фронтенд** | Bootstrap 5, Django Templates |
| **Аутентификация** | JWT (DRF), сессии (шаблоны) |

---

## 📁 Структура проекта
PsyDiary/
├── config/ # Настройки проекта
│ ├── settings.py
│ ├── urls.py
│ ├── celery.py
│ └── wsgi.py
├── users/ # Приложение пользователей
│ ├── models.py # CustomUser, DoctorProfile
│ ├── views.py # Профиль, регистрация, врачи
│ ├── forms.py
│ ├── urls.py
│ └── templates/users/
├── psyhodiary/ # Приложение дневника
│ ├── models.py # Diary, Dream, Habit, TestResult
│ ├── views.py # CRUD, поиск, пагинация
│ ├── urls.py
│ ├── paginators.py
│ └── templates/psyhodiary/
├── pillowtracker/ # Трекер таблеток на данный момент в разработке
│ ├── models.py # Medication, MedicationLog, Alert
│ ├── tasks.py # Celery задачи
│ ├── urls.py
│ └── templates/pillowtracker/
├── nginx/ # Конфигурация Nginx
│ └── nginx.conf
├── templates/ # Общие шаблоны
│ └── base.html
├── static/ # Статические файлы (собираются)
├── staticfiles/ # Собранная статика
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.template
└── README.md # Файл РидМи(этот файл)

---

## 🚀 Установка и запуск

### 📌 Требования

- Docker 20.10+
- Docker Compose 2.0+
- (или Python 3.13+ для запуска без Docker)

### 🐳 Запуск через Docker (рекомендуется)

```bash
# 1. Клонирование репозитория
git clone https://github.com/qjlfvfu/PsyhoDiary.git
cd PsyhoDiary
```
# 2. Настройка переменных окружения
```bash
cp .env.template .env
```
# Отредактируйте .env (укажите пароли, ключи)

# 3. Запуск контейнеров
```bash
docker compose up -d --build
```
# 4. Применение миграций
```bash
docker compose exec backend python manage.py migrate
```
# 5. Сбор статики
```bash
docker compose exec backend python manage.py collectstatic --noinput
```
# 6. Создание суперпользователя
```bash
docker compose exec backend python manage.py createsuperuser
```
🔧 Запуск без Docker (локальная разработка)
```
bash
# 1. Создание виртуального окружения
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. Установка зависимостей
pip install -r requirements.txt

# 3. Настройка .env
cp .env.template .env
# Отредактируйте .env

# 4. Применение миграций и запуск
python manage.py migrate
python manage.py runserver
```
⚙️ Переменные окружения (.env)
Переменная	Описание	Пример
SECRET_KEY	Секретный ключ Django	django-insecure-...
DEBUG	Режим отладки	True / False
ALLOWED_HOSTS	Разрешённые хосты	localhost,127.0.0.1,111.88.254.169
DB_NAME	Имя базы данных	my_diary
DB_USER	Пользователь БД	postgres
DB_PASSWORD	Пароль БД	postgres
DB_HOST	Хост БД (в Docker: db)	db
DB_PORT	Порт БД	5432
REDIS_URL	URL для Redis	redis://redis:6379/0
🌐 Доступ к сайту
Адрес	Описание
http://localhost:8000	Главная страница
http://localhost:8000/admin	Админ-панель
http://localhost:8000/api/schema API документация
http://localhost:8000/api/docs/	Swagger API документация
📦 Управление контейнерами
```
bash
# Запуск всех сервисов
docker compose up -d

# Остановка всех сервисов
docker compose down

# Просмотр логов
docker compose logs -f

# Перезапуск конкретного сервиса
docker compose restart backend

# Выполнение команд внутри контейнера
docker compose exec backend python manage.py shell
```
🧪 Тестирование
``` bash
docker compose exec backend python manage.py test 
```
## 📄 Лицензия
### Проект разработан в рамках дипломной работы. Автор: _Николай Малышкин_

## 📧 Контакты
По вопросам: _**sir.nikolai00@mail.ru**_