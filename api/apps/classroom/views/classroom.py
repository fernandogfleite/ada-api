from api.apps.classroom.models.classroom import (
    Period,
    Room,
)
from api.apps.classroom.serializers.classroom import (
    PeriodSerializer,
    RoomSerializer,
)
from api.apps.authentication.permissions import (
    IsTeacher,
    IsStudent,
    IsSecretary
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class SecretaryMixin:
    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes = (IsAuthenticated, IsSecretary)
        else:
            self.permission_classes = (
                IsAuthenticated, IsTeacher | IsStudent | IsSecretary)

        return super().get_permissions()


class PeriodViewSet(SecretaryMixin,
                    ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = (IsAuthenticated,)


class RoomViewSet(SecretaryMixin,
                  ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = (IsAuthenticated,)
