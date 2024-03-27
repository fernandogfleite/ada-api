from api.apps.classroom.models.classroom import (
    Period,
    Subject,
    Room,
    SubjectPeriod,
    SubjectPeriodWeekday
)

from api.apps.utils.fields import ModifiedRelatedField

from rest_framework.exceptions import ValidationError


class PeriodField(ModifiedRelatedField):
    def get_queryset(self):
        return Period.objects.all()

    def to_representation(self, value):
        return {
            'id': value.id,
            'year': value.year,
            'semester': value.semester,
            'start_date': value.start_date,
            'end_date': value.end_date
        }

    def to_internal_value(self, data):
        try:
            return Period.objects.get(
                id=data
            )

        except Period.DoesNotExist:
            raise ValidationError(
                detail={
                    "detail": "Período não encontrado."
                }
            )


class SubjectField(ModifiedRelatedField):
    def get_queryset(self):
        return Subject.objects.all()

    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'code': value.code,
            'description': value.description,
        }

    def to_internal_value(self, data):
        try:
            return Subject.objects.get(
                id=data
            )

        except Subject.DoesNotExist:
            raise ValidationError(
                detail={
                    "detail": "Disciplina não encontrada."
                }
            )


class RoomField(ModifiedRelatedField):
    def get_queryset(self):
        return Room.objects.all()

    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
        }

    def to_internal_value(self, data):
        try:
            return Room.objects.get(
                id=data
            )

        except Room.DoesNotExist:
            raise ValidationError(
                detail={
                    "detail": "Sala não encontrada."
                }
            )


class SubjectPeriodField(ModifiedRelatedField):
    def get_queryset(self):
        return SubjectPeriod.objects.all()

    def to_representation(self, value):
        return {
            'id': value.id,
            'subject': {
                'id': value.subject.id,
                'name': value.subject.name,
                'code': value.subject.code,
                'description': value.subject.description,
            },
            'period': {
                'id': value.period.id,
                'year': value.period.year,
                'semester': value.period.semester,
            },
            'teacher': {
                'id': value.teacher.user.id,
                'name': value.teacher.user.name,
            },
        }

    def to_internal_value(self, data):
        try:
            return SubjectPeriod.objects.get(
                id=data
            )

        except SubjectPeriod.DoesNotExist:
            raise ValidationError(
                detail={
                    "detail": "Período da disciplina não encontrado."
                }
            )


class SubjectPeriodWeekdayField(ModifiedRelatedField):
    def get_queryset(self):
        return SubjectPeriodWeekday.objects.all()

    def to_representation(self, value):
        return {
            'id': value.id,
            'subject_period': {
                'id': value.subject_period.id,
                'subject': {
                    'id': value.subject_period.subject.id,
                    'name': value.subject_period.subject.name,
                    'code': value.subject_period.subject.code,
                    'description': value.subject_period.subject.description
                },
                'period': {
                    'id': value.subject_period.period.id,
                    'year': value.subject_period.period.year,
                    'semester': value.subject_period.period.semester,
                },
                'teacher': {
                    'id': value.subject_period.teacher.user.id,
                    'name': value.subject_period.teacher.user.name,
                },
            },
            'weekday': {
                'value': value.weekday,
                'label': value.get_weekday_display()
            },
            'start_time': value.start_time,
            'end_time': value.end_time
        }

    def to_internal_value(self, data):
        try:
            return SubjectPeriodWeekday.objects.get(
                id=data
            )

        except SubjectPeriodWeekday.DoesNotExist:
            raise ValidationError(
                detail={
                    "detail": "Dia da semana da disciplina não encontrado."
                }
            )
