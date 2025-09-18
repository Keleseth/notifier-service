from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions, status

from .models import (
    UserContact,
    UserNotificationSettings
)
from .serializers import (
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
