from dataclasses import dataclass
import logging
from typing import Optional, Literal

from celery import shared_task
from django.db import transaction
from django.db.models import QuerySet
from django.utils import timezone

from notifications.models import (
    Notification,
    NotificationStatus,
    UserContact,
    UserNotificationSettings,
)
from notifications.services.delivery_channels import DeliveryService

logger = logging.getLogger(__name__)

Status = Literal[
    'not_found',
    'no_consent',
    'no_contacts',
    'already_sent',
    'sent',
    'failed',
    'processing_set',
]

@dataclass
class SendResult:
    status: Status
    reason: Optional[str] = None


class NotificationSender:
    """
    Управляющий класс - сервис для отправки уведомлений пользователям.
    """

    @staticmethod
    def choose_channel(
            notification: Notification,
            settings: Optional[UserNotificationSettings]
    ) -> Optional[str]:
        if getattr(
            notification,
            'override_channel',
            None
        ):
            return notification.override_channel
        if settings:
            return getattr(
                settings,
                'preferred_notification_channel',
                None
            )
        return None

    @staticmethod
    def _get_and_lock_notification(notification_id: int) -> Notification:
        return (
            Notification.objects
            .select_for_update()
            .select_related('user', 'user__notification_settings')
            .get(pk=notification_id)
        )

    @staticmethod
    def get_active_contacts(user) -> QuerySet[UserContact]:
        return user.contacts.filter(is_active=True, is_verified=True)

    # duplicate method removed below; keeping a single definition above

    @classmethod
    def process(cls, notification_id: int) -> SendResult:
        with transaction.atomic():
            try:
                note = cls._get_and_lock_notification(notification_id)
            except Notification.DoesNotExist:
                return SendResult('not_found', 'Уведомление не найдено')

            if note.status == NotificationStatus.SENT:
                return SendResult('already_sent', 'Уже отправлено')

            settings = getattr(
                note.user,
                'notification_settings',
                None
            )
            if not getattr(
                settings,
                'notification_consent',
                False
            ):
                return SendResult('no_consent')

            contacts = cls.get_active_contacts(note.user)
            if not contacts.exists():
                return SendResult('no_contacts', 'Нет активных контактов')

            # выбор канала
            channel = cls.choose_channel(note, settings)
            if channel not in DeliveryService.CHANNELS:
                return SendResult('failed', f'Несуществующий канал {channel}')
            if not channel:
                return SendResult('failed', 'Нет канала для отправки')

            # пометим processing
            note.status = NotificationStatus.PROCESSING     
            if hasattr(note, 'updated_at'):
                note.updated_at = timezone.now()
            note.save(
                update_fields=[
                    'status',
                    'updated_at'
                ] if hasattr(note, 'updated_at') else ['status']
            )

        try:
            result = DeliveryService.deliver_with_fallback(
                channel,
                contacts,
                note.subject,
                note.body
            )

            if not result.ok:
                logger.warning('DeliveryService reported failure: %s', result.reason)
                with transaction.atomic():
                    try:
                        fresh = Notification.objects.select_for_update().get(
                            pk=notification_id
                        )
                        fresh.status = NotificationStatus.FAILED
                        if hasattr(fresh, 'updated_at'):
                            fresh.updated_at = timezone.now()
                        fresh.save(
                            update_fields=['status', 'updated_at'] if hasattr(
                                fresh,
                                'updated_at'
                            ) else ['status']
                        )
                    except Notification.DoesNotExist:
                        pass
                return SendResult('failed', result.reason)

            fields = ['status']
            note.status = NotificationStatus.SENT
            if hasattr(
                note, 'updated_at'
            ): note.updated_at = timezone.now(); fields.append('updated_at')
            if hasattr(
                note, 'sent_at'
            ): note.sent_at = timezone.now(); fields.append('sent_at')
            note.save(update_fields=fields)
            return SendResult('sent')
        except Exception as e:
            logger.exception('Delivery failed for %s: %s', note.pk, e)
            with transaction.atomic():
                try:
                    fresh = Notification.objects.select_for_update().get(
                        pk=notification_id
                    )
                    fresh.status = NotificationStatus.FAILED
                    if hasattr(
                        fresh,
                        'updated_at'
                    ): fresh.updated_at = timezone.now()
                    fresh.save(
                        update_fields=['status', 'updated_at'] if hasattr(
                            fresh,
                            'updated_at'
                        ) else ['status']
                    )
                except Notification.DoesNotExist:
                    pass
                return SendResult('failed', str(e))


@shared_task
def send_notification_task(notification_id):
    sender = NotificationSender()
    result = sender.process(notification_id)
    return result.status