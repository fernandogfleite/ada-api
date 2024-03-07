from api.apps.classroom.models.classroom import (
    Period,
    Subject,
    Room,
    SubjectPeriod,
    SubjectPeriodWeekday
)

from api.apps.utils.fields import ModifiedRelatedField


class PeriodField(ModifiedRelatedField):
    def get_queryset(self):
        return Period.objects.all()

    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'start_time': value.start_time,
            'end_time': value.end_time
        }

    def to_internal_value(self, data):
        try:
            return Period.objects.get(
                id=data
            )

        except Period.DoesNotExist:
            self.fail('does_not_exist', pk_value=data)


class SubjectField(ModifiedRelatedField):
    def get_queryset(self):
        return Subject.objects.all()

    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'code': value.code
        }

    def to_internal_value(self, data):
        try:
            return Subject.objects.get(
                id=data
            )

        except Subject.DoesNotExist:
            self.fail('does_not_exist', pk_value=data)


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
            self.fail('does_not_exist', pk_value=data)


class SubjectPeriodField(ModifiedRelatedField):
    def get_queryset(self):
        return SubjectPeriod.objects.all()

    def to_representation(self, value):
        return {
            'id': value.id,
            'subject': {
                'id': value.subject.id,
                'name': value.subject.name,
                'code': value.subject.code
            },
            'period': {
                'id': value.period.id,
                'name': value.period.name,
            }
        }

    def to_internal_value(self, data):
        try:
            return SubjectPeriod.objects.get(
                id=data
            )

        except SubjectPeriod.DoesNotExist:
            self.fail('does_not_exist', pk_value=data)


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
                    'code': value.subject_period.subject.code
                },
                'period': {
                    'id': value.subject_period.period.id,
                    'name': value.subject_period.period.name,
                }
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
            self.fail('does_not_exist', pk_value=data)
