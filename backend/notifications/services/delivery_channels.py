from dataclasses import dataclass
import logging
from typing import (
    ClassVar,
    Mapping,
    Optional,
    Protocol,
    Sequence,
)

from django.db.models import QuerySet

from notifications.models import UserContact


logger = logging.getLogger(__name__)


class DeliverFunc(Protocol):
    def __call__(self, to: str, subject: Optional[str], body: str) -> bool:
        pass

def send_email(to_address, subject, body):
    """
    Заглушка функции отправки email.
    """
    print(
        f'Отправка email на {to_address} '
        f'с темой "{subject}" и текстом "{body}"'
    )
    logger.info(
        f'Отправка email на {to_address} '
        f'с темой "{subject}" и текстом "{body}"'
    )
    return True

def send_sms(to_number, subject, body):
    """
    Заглушка функции отправки sms-сообщения.
    """
    print(f'Отправка SMS на {to_number} с текстом "{body}"')
    logger.info(
        f'Отправка SMS на {to_number} с текстом "{body}"'
    )
    return True

def send_to_telegram(to_user, title, body):
    """
    Заглушка функции отправки сообщения в Telegram по id.
    """
    print(
        f'Отправка сообщения в Telegram пользователю {to_user}'
        f' с текстом "{body}"'
    )
    logger.info(
        f'Отправка сообщения в Telegram пользователю {to_user}'
        f' с текстом "{body}"'
    )
    return True


@dataclass(frozen=True, slots=True)
class DeliveryResult:
    ok: bool
    channel: Optional[str] = None
    sent_count: int = 0
    reason: Optional[str] = None

class DeliveryService:
    """
    Сервис доставки уведомлений по разным каналам.
    """

    CHANNELS: ClassVar[Mapping[str, DeliverFunc]] = {
        "email": send_email,
        "phone_number": send_sms,
        "telegram": send_to_telegram,
    }

    @classmethod
    def deliver_with_fallback(
        cls,
        primary_channel: str,
        contacts: QuerySet[UserContact],
        subject: Optional[str],
        body: str,
        fallback_order: Sequence[str] = ('email', 'phone_number', 'telegram'),
    ) -> DeliveryResult:
        """
        Метод пытается доставить уведомление через предпочитаемый канал,
        если не получается, то через запасные каналы по порядку.
        """

        if primary_channel not in cls.CHANNELS:
            return DeliveryResult(
                False,
                reason=f'unknown primary channel {primary_channel}'
            )

        order = [primary_channel] + [
            ch for ch in fallback_order if ch != primary_channel
        ]

        last_error: Optional[str] = None
        for channel in order:
            fn = cls.CHANNELS.get(channel)
            if fn is None:
                continue
            chan_contacts = contacts.filter(contact_type=channel)
            if not chan_contacts.exists():
                continue

            successes = 0
            for c in chan_contacts.iterator():
                try:
                    ok = fn(c.normalized_value, subject, body)
                except Exception as e:
                    logger.error(f'Ошибка отправки через {channel} для {c.normalized_value}: {e}')
                    ok = False
                if ok:
                    successes += 1
                else:
                    logger.warning(f'Не удалось отправить через {channel} для {c.normalized_value}')

            if successes > 0:
                return DeliveryResult(True, channel=channel, sent_count=successes)

            logger.info(f'Нет успешных доставок через канал {channel}')
            last_error = f'no successful deliveries via {channel}'

        logger.error(f'Доставка не удалась ни по одному каналу: {last_error or "no contacts / no channels"}')
        return DeliveryResult(False, reason=last_error or 'no contacts / no channels')

