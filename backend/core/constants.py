# регулярки
PHONE_NUMBER_PATTERN = r'^\+\d{7,15}$'
TELEGRAM_ID_PATTERN = r'^\+?\d{7,11}$'

# тексты ошибок
INVALID_NUMBER = 'Введите валидный номер телефона, пример: +1234567890.'
INVALID_TELEGRAM_ID = 'Введите валидный Telegram ID состоящий из цифр.'
NO_CONTACT_VALUE = (
    'Укажите как минимум один доступный способ связи.'
    ' Пример: {"email": "example@example.com"}'
)
INVALID_PREFFERED_CHANEL = (
    'Разрешенные каналы: email, telegram, телефонный номер.'
)
INVALID_CONFIRMATION = (
    'Поле согласия на уведомления должно содержать true или false'
)