from api.apps.classroom.models.classroom import (
    Period,
    Room,
    Subject,
    SubjectPeriod,
    SubjectPeriodStudent,
    Classroom
)
from api.apps.classroom.serializers.classroom import (
    PeriodSerializer,
    RoomSerializer,
    SubjectSerializer,
    SubjectPeriodSerializer,
    SubjectPeriodStudentSerializer,
    ClassroomSerializer
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
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import status

from django.db.models import Q

from datetime import datetime


class SecretaryMixin:
    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes = (IsAuthenticated, IsSecretary)
        else:
            self.permission_classes = (
                IsAuthenticated,
                IsTeacher | IsStudent | IsSecretary
            )

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

            if self.request.user.is_student:
                queryset = queryset.exclude(
                    id__in=SubjectPeriodStudent.objects.filter(
                        student__user_id=self.request.user.id
                    ).values('subject_period_id')
                )

        return queryset.filter(query).order_by(
            'subject__name',
            'period__year',
            'period__semester'
        )


class SubjectPeriodStudentViewSet(CreateModelMixin,
                                  ListModelMixin,
                                  RetrieveModelMixin,
                                  DestroyModelMixin,
                                  GenericViewSet):
    queryset = SubjectPeriodStudent.objects.all()
    serializer_class = SubjectPeriodStudentSerializer
    permission_classes = (
        IsAuthenticated,
        IsStudent | IsSecretary | IsTeacher
    )

    def get_queryset(self):
        queryset = super().get_queryset()

        query = Q()

        if self.action == 'list':
            student_id = self.request.query_params.get('student_id')
            subject_period_id = self.kwargs.get('subject_period_id')

            if not self.request.user.is_student:
                if student_id:
                    query &= Q(student_id=student_id)

            if subject_period_id:
                query &= Q(subject_period_id=subject_period_id)

        return queryset.filter(query).order_by('id')

    def create(self, request, *args, **kwargs):
        data = dict(**request.data)
        if request.user.is_student:
            data['student'] = request.user.id

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class ClassroomViewSet(ModelViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.action in ('create', 'update', 'partial_update', 'destroy'):
            self.permission_classes = (
                IsAuthenticated,
                IsTeacher | IsSecretary
            )
        else:
            self.permission_classes = (
                IsAuthenticated,
                IsTeacher | IsStudent | IsSecretary
            )

        return super().get_permissions()


class ListLoggedUserSubjectPeriods(ListModelMixin,
                                   GenericViewSet):
    queryset = SubjectPeriod.objects.all()
    serializer_class = SubjectPeriodSerializer
    permission_classes = (IsAuthenticated, IsTeacher | IsStudent | IsSecretary)

    def get_queryset(self):
        queryset = super().get_queryset()

        query = Q()

        if self.request.user.is_teacher:
            query &= Q(teacher_id=self.request.user.id)

        elif self.request.user.is_student:
            query &= Q(
                id__in=SubjectPeriodStudent.objects.filter(
                    student__user_id=self.request.user.id
                ).values('subject_period_id')
            )

        return queryset.filter(query).order_by(
            'period__year',
            'period__semester',
            'subject__name'
        )


class ListLoggedUserClassrooms(ListModelMixin,
                               GenericViewSet):
    queryset = Classroom.objects.all()
    serializer_class = ClassroomSerializer
    permission_classes = (IsAuthenticated, IsTeacher | IsStudent | IsSecretary)

    def get_queryset(self):
        queryset = super().get_queryset()

        query = Q()

        try:
            start_date = datetime.strptime(
                self.request.query_params.get('start_date'),
                '%Y-%m-%d'
            )
            end_date = datetime.strptime(
                self.request.query_params.get('end_date'),
                '%Y-%m-%d'
            )

            query &= Q(
                date__gte=start_date,
                date__lte=end_date
            )

        except:
            raise ValidationError(
                {
                    'detail': 'Data inválida. Formato esperado: YYYY-MM-DD.'
                }
            )

        if self.request.user.is_teacher:
            query &= Q(
                subject_period_weekday__subject_period__teacher__user_id=self.request.user.id)

        elif self.request.user.is_student:
            query &= Q(
                subject_period_weekday__subject_period_id__in=SubjectPeriodStudent.objects.filter(
                    student__user_id=self.request.user.id
                ).values('subject_period_id')
            )

        return queryset.filter(query).order_by(
            'date',
            'start_time',
            'end_time'
        )


class ListStudentInSubjectPeriod(ListModelMixin,
                                 GenericViewSet):
    queryset = SubjectPeriodStudent.objects.all()
    serializer_class = SubjectPeriodStudentSerializer
    permission_classes = (IsAuthenticated, IsTeacher | IsSecretary)

    def get_queryset(self):
        queryset = super().get_queryset()

        query = Q()

        subject_period_id = self.kwargs.get('subject_period_id')

        if subject_period_id:
            query &= Q(subject_period_id=subject_period_id)

        if self.request.user.is_teacher:
            query &= Q(subject_period__teacher__user_id=self.request.user.id)

        return queryset.filter(query).order_by('id')
