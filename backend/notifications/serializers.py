# from django.core.validators import RegexValidator
from rest_framework import serializers

from .models import (
    ContactType,
    UserContact,
    UserNotificationSettings,
)
from core.constants import (
    INVALID_CONFIRMATION,
    INVALID_NUMBER,
    INVALID_TELEGRAM_ID,
    NO_CONTACT_VALUE,
    PHONE_NUMBER_PATTERN,
    TELEGRAM_ID_PATTERN,
    INVALID_PREFFERED_CHANEL
)


class UserNotificationSettingsSerializer(serializers.ModelSerializer):
    preferred_notification_channel = serializers.ChoiceField(
        choices=ContactType.choices,
        error_messages={
            'invalid_choice': INVALID_PREFFERED_CHANEL,
        },
    )
    notification_consent = serializers.BooleanField(
        required=False,
        default=False,
        error_messages={
                'invalid': INVALID_CONFIRMATION,
        },
    )
    class Meta:
        model = UserNotificationSettings
        fields = (
            'preferred_notification_channel',
            'notification_consent',
        )
        read_only_fields = ('created_at', 'updated_at')


class UserContactUpdateSerializer(serializers.Serializer):
    email = serializers.EmailField(required=False)
    phone_number = serializers.RegexField(
        regex=PHONE_NUMBER_PATTERN,
        required=False,
        error_messages={
            'invalid': INVALID_NUMBER
        },
    )
    telegram = serializers.RegexField(
        regex=TELEGRAM_ID_PATTERN,
        required=False,
        error_messages={
            'invalid': INVALID_TELEGRAM_ID
        },
    )

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(NO_CONTACT_VALUE)
        return attrs

    def save(self):
        user = self.context['request'].user
        updated = []

        mapping = {
            'email': ContactType.EMAIL,
            'phone_number': ContactType.PHONE_NUMBER,
            'telegram': ContactType.TELEGRAM,
        }

        for field, ctype in mapping.items():
            if field not in self.validated_data:
                continue
            value = self.validated_data[field]

            obj, created = UserContact.objects.get_or_create(
                user=user,
                contact_type=ctype,
                defaults={'value': value, 'normalized_value': value},
            )
            if not created:
                obj.value = value
                obj.normalized_value = value
                obj.save(update_fields=['value', 'normalized_value', 'updated_at'])

            updated.append(obj)

        return updated


class UserContactReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserContact
        fields = (
            'contact_type', 'normalized_value',
        )
