# Copilot Instructions for notifier-service

## Project Overview
This is a Django-based notification service. The main components are:
- `core/`: Shared constants and utilities.
- `notifications/`: App for notification logic, including models, serializers, views, and services.
- `notifier_service/`: Django project settings and entry points.

## Architecture & Data Flow
- Notifications are managed in `notifications/models.py` and exposed via API endpoints in `notifications/views.py`.
- Business logic is separated into `notifications/services/notifications.py`.
- Database migrations are tracked in `notifications/migrations/`.
- The SQLite database is at `backend/db.sqlite3`.

## Developer Workflows
- **Run server:**
  ```bash
  cd backend
  python manage.py runserver
  ```
- **Run tests:**
  ```bash
  cd backend
  python manage.py test notifications
  ```
- **Apply migrations:**
  ```bash
  cd backend
  python manage.py migrate
  ```
- **Create migrations:**
  ```bash
  cd backend
  python manage.py makemigrations notifications
  ```

## Conventions & Patterns
- Business logic is kept out of views; use `services/` for non-trivial operations.
- Serializers in `notifications/serializers.py` handle input/output validation.
- API endpoints are defined in `notifications/views.py` and routed via `notifications/urls.py`.
- Settings and configuration are in `notifier_service/settings.py`.
- Use constants from `core/constants.py` for shared values.

## Integration Points
- External dependencies are listed in `requirements.txt`.
- The project uses Django ORM for database access.
- All notification-related logic should be added to the `notifications` app.

## Examples
- To add a new notification type, update `models.py`, create a serializer, and add logic in `services/notifications.py`.
- For new API endpoints, add a view in `views.py` and route it in `urls.py`.

---
If any section is unclear or missing, please provide feedback for further refinement.