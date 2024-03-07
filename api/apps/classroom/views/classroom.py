from api.apps.classroom.models.classroom import (
    Period,
)
from api.apps.classroom.serializers.classroom import (
    PeriodSerializer,
)
from api.apps.authentication.permissions import (
    IsTeacher,
    IsStudent,
    IsSecretary
)

from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated


class PeriodViewSet(ModelViewSet):
    queryset = Period.objects.all()
    serializer_class = PeriodSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes = (IsAuthenticated, IsSecretary)
        else:
            self.permission_classes = (IsAuthenticated,)

        return super().get_permissions()
