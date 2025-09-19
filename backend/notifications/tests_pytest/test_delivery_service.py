import pytest

from notifications.models import NotificationStatus
from notifications.services.delivery_channels import DeliveryService
from notifications.services.notifications import NotificationSender

def fake_fail(*a, **k): return False
def fake_ok(*a, **k): return True


@pytest.mark.django_db
def test_process_success(
    contact_email,
    notification_settings,
    notification,
    monkeypatch
):
    monkeypatch.setattr(
        'notifications.services.delivery_channels.DeliveryService.deliver_with_fallback',
        lambda *a, **kw: type('Result', (), {'ok': True, 'channel': 'email', 'sent_count': 1})()
    )
    # Привязываем настройки к пользователю
    notification.user.notification_settings = notification_settings
    notification.user.save()
    res = NotificationSender.process(notification.id)
    assert res.status == 'sent'
    notification.refresh_from_db()
    assert notification.status == NotificationStatus.SENT


@pytest.mark.django_db
def test_process_no_contacts(
    notification_settings,
    notification,
    user
):
    # Без контактов
    notification.user.notification_settings = notification_settings
    notification.user.save()
    res = NotificationSender.process(notification.id)
    assert res.status == 'no_contacts'


@pytest.mark.django_db
def test_failed_first_channel_second_success(
    all_contacts,
    notification_settings,
    notification,
    monkeypatch
):
    monkeypatch.setattr(
        'notifications.services.delivery_channels.send_to_telegram',
        fake_fail
    )
    monkeypatch.setattr(
        'notifications.services.delivery_channels.send_email',
        fake_ok
    )
    monkeypatch.setattr(
        'notifications.services.delivery_channels.send_sms',
        fake_fail
    )

    # Переписываем ссылки внутри CHANNELS, чтобы мок фунекций сработал
    monkeypatch.setitem(DeliveryService.CHANNELS, 'email', fake_fail)
    monkeypatch.setitem(DeliveryService.CHANNELS, 'telegram', fake_ok)
    monkeypatch.setitem(DeliveryService.CHANNELS, 'phone_number', fake_fail)
    result = NotificationSender.process(notification.id)
    assert result.status == NotificationStatus.SENT
    assert result.channel == 'telegram'


@pytest.mark.django_db
def test_all_channels_failed(
    all_contacts,
    notification_settings,
    notification,
    monkeypatch
):
    # Все каналы возвращают False
    monkeypatch.setattr(
        'notifications.services.delivery_channels.send_to_telegram',
        lambda *a, **k: False
    )
    monkeypatch.setattr(
        'notifications.services.delivery_channels.send_email',
        lambda *a, **k: False
    )
    monkeypatch.setattr(
        'notifications.services.delivery_channels.send_sms',
        lambda *a, **k: False
    )
    # Переписываем ссылки внутри CHANNELS, чтобы мок сработал
    monkeypatch.setitem(DeliveryService.CHANNELS, 'email', fake_fail)
    monkeypatch.setitem(DeliveryService.CHANNELS, 'telegram', fake_fail)
    monkeypatch.setitem(DeliveryService.CHANNELS, 'phone_number', fake_fail)
    result = NotificationSender.process(notification.id)
    assert result.status == NotificationStatus.FAILED
    assert result.reason is not None


@pytest.mark.django_db
def test_no_consent(
    contact_email,
    notification_settings_no_consent,
    notification
):
    notification.user.notification_settings = notification_settings_no_consent
    notification.user.save()
    result = NotificationSender.process(notification.id)
    assert result.status == 'no_consent'


@pytest.mark.django_db
def test_not_active_contact(
    contact_email,
    notification_settings,
    notification
):
    contact_email.is_active = False
    contact_email.save()
    notification.user.notification_settings = notification_settings
    notification.user.save()
    result = NotificationSender.process(notification.id)
    assert result.status == 'no_contacts'


@pytest.mark.django_db
def test_only_verified_contacts(
    all_unverified_contacts,
    notification_settings,
    notification
):
    notification.user.notification_settings = notification_settings
    notification.user.save()
    result = NotificationSender.process(notification.id)
    assert result.status == 'no_contacts'
