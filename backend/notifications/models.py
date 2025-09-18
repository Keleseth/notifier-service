from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class ContactType(models.TextChoices):
    """
    Enum модель для опций связи с пользователем.
    """
    EMAIL = 'email', 'Email'
    TELEGRAM = 'telegram', 'Telegram'
    PHONE_NUMBER = 'phone_number', 'Phone_number'


class UserNotificationSettings(models.Model):
    """
    Модель настроек уведомлений пользователя.

    Поля:
        - user, ссылка на пользователя
        - preferred_notification_channel, предпочитаемый способ уведомления
        - notification_concent, согласие на получение уведомлений
        - created_ad, дата создания настроек
        - updated_at, дата обновления настроек.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='notification_settings',
    )
    preferred_notification_channel = models.CharField(
        max_length=24,
        choices=ContactType.choices,
        default=ContactType.EMAIL,
    )
    notification_consent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    class Meta:
        verbose_name = 'настройка уведомления'
        verbose_name_plural = 'Настройки уведомлений'

    def __str__(self):
        return (
            f'{self.user}, {self.preferred_notification_channel})'
        )


class UserContact(models.Model):
    """
    Модель контактов пользователя.

    Поля:
        - user, ссылка на пользователя
        - contact_type, тип контакта (почта, телеграм, мобильный ...)
        - value, переданная пользователем строка контакта
        - normalized_value, строка контакта после приведения к стандарту
        - is_active, состояние активности контакта на данный момент
        - is_verified, подтвержден ли контакт пользователем
        - create_at, дата создания контакта
        - updated_at, дата обновления контакта.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='contacts',
    )
    contact_type = models.CharField(
        max_length=32,
        choices=ContactType.choices,
    )
    value = models.CharField(
        max_length=128,
        help_text='Строка контакта переданная пользователем',
    )
    normalized_value = models.CharField(
        max_length=128,
        editable=False,
        db_index=True,
        help_text='Строка контакта после приведения к стандарту',
    )
    is_active = models.BooleanField(
        default=True,
        help_text='Активен ли канал(для сервиса рассылки)',
    )
    is_verified = models.BooleanField(
        default=False,
        help_text='Подтверждение контакта пользователем',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['contact_type', 'id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'contact_type'],
                name='uniq_user_contact_type',
            ),
            models.UniqueConstraint(
                fields=['contact_type', 'normalized_value'],
                condition=models.Q(is_verified=True),
                name='uniq_verified_contact_value',
            ),
        ]

    # def clean(self):
    #     """
    #     Нормализует и валидирует данные контакта.
    #     """
    #     # TODO добавить приведение к стандарту на уровне базы, пока только 
    #     # на уровне api
    #     # from .utils import normalize_contact, validate_contact
    #     # norm = normalize_contact(self.contact_type, self.value)
    #     # validate_contact(self.contact_type, norm)
    #     # self.normalized_value = norm

    # def __str__(self):
    #     return f'{self.user}:{self.contact_type}-{self.normalized_value}'
