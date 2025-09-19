# Notifier Service

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Django](https://img.shields.io/badge/django-092E20?style=for-the-badge&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/djangorestframework-E74C3C?style=for-the-badge&logo=django&logoColor=white)
![Celery](https://img.shields.io/badge/celery-37814A?style=for-the-badge&logo=celery&logoColor=white)
![Redis](https://img.shields.io/badge/redis-DC382D?style=for-the-badge&logo=redis&logoColor=white)
![SQLite](https://img.shields.io/badge/sqlite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)

## Project Description

Notifier is a backend service for delivering user notifications via multiple channels (email / Telegram / SMS) with fallback logic, queuing, and status tracking.

## Quick Start

1. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

2. Apply migrations:
    ```bash
    cd backend
    python manage.py migrate
    ```

3. Start the server:
    ```bash
    cd backend
    python manage.py runserver
    ```

4. Start the Celery worker (if needed):
    ```bash
    cd backend
    celery -A notifier_service worker -l info
    ```

5. Run tests:
    ```bash
    cd backend
    pytest -s notifications/tests_pytest
    ```

## Project Status
The project is under active development. Notification delivery functionality is currently stubbed.  
Plans include adding more channels and making all channels fully operational.

## Project Structure

- `backend/core/` — constants and utilities
- `backend/notifications/` — business logic, models, serializers, services, tests
- `backend/notifier_service/` — Celery worker for processing and sending notifications

## Features

- Fallback delivery via multiple channels
- Logging of successful and failed attempts
- Test coverage for main scenarios
- SQLite for data storage

### Developed by:

- Alexander Kelesidis [Keleseth](https://github.com/Keleseth)

## Contacts

For questions and suggestions: [Keleseth](https://github.com/Keleseth)