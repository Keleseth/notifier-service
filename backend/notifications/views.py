from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from notifications.services.notifications import send_notification_task
from .models import (
    UserContact,
    UserNotificationSettings
)
from .serializers import (
    NotificationCreateSerializer,
    UserContactReadSerializer,
    UserContactUpdateSerializer,
    UserNotificationSettingsSerializer,
)


class MyNotificationSettingsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        obj, _ = UserNotificationSettings.objects.get_or_create(
            user=request.user
        )
        return Response(
            UserNotificationSettingsSerializer(obj).data
        )

    def patch(self, request):
        obj, _ = UserNotificationSettings.objects.get_or_create(
            user=request.user
        )
        serializer = UserNotificationSettingsSerializer(
            obj,
            data=request.data,
            partial=True
        )
        serializer.is_valid(
            raise_exception=True
        )
        serializer.save()
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class MyContactsView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        queryset = UserContact.objects.filter(
            user=request.user
        ).order_by('created_at')
        data = UserContactReadSerializer(queryset, many=True).data
        return Response(data)

    def patch(self, request):
        serializer = UserContactUpdateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        queryset = UserContact.objects.filter(
            user=request.user
        ).order_by('created_at')
        return Response(
            UserContactReadSerializer(queryset, many=True).data,
            status=status.HTTP_200_OK
        )


class MyNorificationView(APIView):

    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = NotificationCreateSerializer(data=request.data)
        serializer = NotificationCreateSerializer(
            data=request.data,
            context={"request": request},
        )
        serializer.is_valid(raise_exception=True)
        notification = serializer.save()
        send_notification_task.delay(notification.id)
        return Response(
            {
                'accepted': True,
                'payload': serializer.data,
                'queued': True, # Задача поставлена в очередь
            },
            status=status.HTTP_202_ACCEPTED,
        )
