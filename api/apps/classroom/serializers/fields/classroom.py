from api.apps.classroom.models.classroom import (
    Period,
    Subject,
    Room
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
