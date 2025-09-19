import pytest
from django.contrib.auth import get_user_model
from notifications.models import (
    ContactType,
    Notification,
    UserContact,
    UserNotificationSettings,
)


@pytest.fixture
def user(db):
    return get_user_model().objects.create_user(
        username='testuser',
        email='test@example.com',
        password='password'
    )


@pytest.fixture
def all_contacts(user):
    return [
        UserContact.objects.create(
            user=user,
            contact_type=ContactType.EMAIL,
            value='test@example.com',
            normalized_value='test@example.com',
            is_verified=True,
            is_active=True
        ),
        UserContact.objects.create(
            user=user,
            contact_type=ContactType.PHONE_NUMBER,
            value='+1234567890',
            normalized_value='+1234567890',
            is_verified=True,
            is_active=True
        ),
        UserContact.objects.create(
            user=user,
            contact_type=ContactType.TELEGRAM,
            value='7777777777',
            normalized_value='7777777777',
            is_verified=True,
            is_active=True
        ),
    ]


@pytest.fixture
def all_unverified_contacts(user):
    from notifications.models import UserContact, ContactType
    return [
        UserContact.objects.create(
            user=user,
            contact_type=ContactType.EMAIL,
            value='unverified@example.com',
            normalized_value='unverified@example.com',
            is_verified=False,
            is_active=True
        ),
        UserContact.objects.create(
            user=user,
            contact_type=ContactType.PHONE_NUMBER,
            value='+79991234567',
            normalized_value='+79991234567',
            is_verified=False,
            is_active=True
        ),
        UserContact.objects.create(
            user=user,
            contact_type=ContactType.TELEGRAM,
            value='@unverifieduser',
            normalized_value='@unverifieduser',
            is_verified=False,
            is_active=True
        ),
    ]


@pytest.fixture
def contact_email(user):
    return UserContact.objects.create(
        user=user,
        contact_type=ContactType.EMAIL,
        value='test@example.com',
        normalized_value='test@example.com',
        is_verified=True,
        is_active=True
    )


@pytest.fixture
def notification_settings(user):
    return UserNotificationSettings.objects.create(
        user=user,
        preferred_notification_channel=ContactType.EMAIL,
        notification_consent=True
    )


@pytest.fixture
def notification(user):
    return Notification.objects.create(
        user=user,
        subject='Test',
        body='Test body'
    )


@pytest.fixture
def notification_settings_no_consent(user):
    return UserNotificationSettings.objects.create(
        user=user,
        preferred_notification_channel='email',
        notification_consent=False
    )