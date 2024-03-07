from api.apps.classroom.models.classroom import (
    Period,
    Room,
    Subject,
    SubjectPeriod
)
from api.apps.classroom.serializers.classroom import (
    PeriodSerializer,
    RoomSerializer,
    SubjectSerializer,
    SubjectPeriodSerializer
)
from api.apps.authentication.permissions import (
    IsTeacher,
    IsStudent,
    IsSecretary
)

from rest_framework.viewsets import (
    ModelViewSet,
    GenericViewSet
)
from rest_framework.mixins import (
    CreateModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    DestroyModelMixin
)
from rest_framework.permissions import IsAuthenticated

from django.db.models import Q


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


class SubjectViewSet(SecretaryMixin,
                     ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (IsAuthenticated,)


class SubjectPeriodViewSet(SecretaryMixin,
                           CreateModelMixin,
                           ListModelMixin,
                           RetrieveModelMixin,
                           DestroyModelMixin,
                           GenericViewSet):
    queryset = SubjectPeriod.objects.all()
    serializer_class = SubjectPeriodSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        queryset = super().get_queryset()

        query = Q()

        if self.action == 'list':
            teacher_id = self.request.query_params.get('teacher_id')
            period_id = self.request.query_params.get('period_id')

            if teacher_id:
                query &= Q(teacher_id=teacher_id)

            if period_id:
                query &= Q(period_id=period_id)

        return queryset.filter(query).order_by('id')
