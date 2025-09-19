# Notifier Service

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/djangorestframework-E74C3C?style=for-the-badge&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

## Описание проекта

Notifier — backend‑сервис для доставки пользовательских уведомлений по различным каналам (email / Telegram / SMS) с fallback‑логикой, очередями и записью статусов.

## Быстрый старт

1. Установите зависимости:
    ```bash
    pip install -r requirements.txt
    ```

2. Примените миграции:
    ```bash
    cd backend
    python manage.py migrate
    ```

3. Запустите сервер:
    ```bash
    cd backend
    python manage.py runserver
    ```

4. Запустите Celery worker (если требуется):
    ```bash
    cd backend
    celery -A notifier_service worker -l info
    ```

5. Запустите тесты:
    ```bash
    cd backend
    pytest -s notifications/tests_pytest
    ```

## Статус проекта
Проект в активной разработке. Функционал по доставки самих уведомлений пока на заглушках.  
В планах поднять кол-во каналов, перевести все каналы в рабочее состояние.


## Структура проекта

- `backend/core/` — константы и утилиты
- `backend/notifications/` — бизнес-логика, модели, сериализаторы, сервисы, тесты
- `backend/notifier_service/` — Celery worker по обработке и отправке уведомлений

## Особенности

- Fallback-отправка по нескольким каналам
- Логирование успешных и неуспешных попыток
- Покрытие тестами основных сценариев
- SQLite для хранения данных

### Проект разработан:

- Разработчик Келесидис Александр [Keleseth](https://github.com/Keleseth)


## Контакты

Для вопросов и предложений: [Keleseth](https://github.com/Keleseth)