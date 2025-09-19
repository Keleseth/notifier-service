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

## Шаги для проверки функционала вручную
### Джанго и Celery + Redis должны быть запущены
### API документация http://127.0.0.1:8000/api/docs/
1. Создать пользователя POST http://127.0.0.1:8000/auth/users/ или через sql-client к примеру SQLiteStudio
2. Получить JWT токен POST http://127.0.0.1:8000/auth/jwt/create (использовать access токен во всех посл. запросах в заголовке Authorization: Bearer)
3. Добавить контакт(ы) для текущего пользователя PATCH http://127.0.0.1:8000/api/me/contacts/ (перевести их в состояние is_verified, is_active через тот же SQLiteStudio)
4. По адресу http://127.0.0.1:8000/api/me/notification-settings/ подтвердить согласие на получение уведомлений, а также по желанию указать настройки для уведомлений.
5. Создать уведомление http://127.0.0.1:8000/api/me/notifications/, процесс запустит работу Celery и отправку уведомлений (заглушка)
6. Логи в проекте по адресу logs/delivery

### Запуск тестов
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