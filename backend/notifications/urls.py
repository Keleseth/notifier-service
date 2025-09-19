from django.urls import path

from .views import (
    MyContactsView,
    MyNotificationSettingsView,
    MyNorificationView
)


urlpatterns = [
    path('me/contacts/', MyContactsView.as_view(), name='my-contacts'),
    path(
        'me/notification-settings/',
        MyNotificationSettingsView.as_view(),
        name='my-notification-settings'
    ),
    path('me/notifications/', MyNorificationView.as_view(), name='my-notifications'),
]
