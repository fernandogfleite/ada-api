from api.apps.authentication.models.user import (
    Teacher,
    Student
)
from api.apps.utils.fields import ModifiedRelatedField


class TeacherField(ModifiedRelatedField):
    def get_queryset(self):
        return Teacher.objects.all()

    def to_representation(self, value):
        return {
            'id': value.user.id,
            'name': value.user.name,
        }

    def to_internal_value(self, data):
        try:
            return Teacher.objects.get(
                user_id=data,
                user__is_active=True,
                user__is_confirmed=True
            )

        except Teacher.DoesNotExist:
            self.fail('does_not_exist', pk_value=data)


class StudentField(ModifiedRelatedField):
    def get_queryset(self):
        return Student.objects.all()

    def to_representation(self, value):
        return {
            'id': value.id,
            'name': value.name,
            'registration_id': value.registration_id,
        }

    def to_internal_value(self, data):
        try:
            return Student.objects.get(
                id=data,
                user__is_active=True,
                user__is_confirmed=True
            )

        except Student.DoesNotExist:
            self.fail('does_not_exist', pk_value=data)
