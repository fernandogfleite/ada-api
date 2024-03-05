from rest_framework import (
    status,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response

from api.apps.authentication.permissions import IsSecretary
from api.apps.authentication.serializers.user import (
    CreateSecretarySerializer,
    CreateStudentSerializer,
    CreateTeacherSerializer
)


class CreateUserViewSet(CreateModelMixin, GenericViewSet):
    message = ""

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)

        data = {
            "message": self.message
        }

        return Response(
            data,
            status=status.HTTP_201_CREATED,
            headers=headers
        )


class StudentRegisterViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CreateStudentSerializer
    message = "Estudante criado com sucesso. Por favor, verifique seu email."


class SecretaryRegisterViewSet(CreateModelMixin, GenericViewSet):
    serializer_class = CreateSecretarySerializer
    message = "Secretário criado com sucesso. Por favor, verifique seu email."


class TeacherRegisterViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated, IsSecretary]
    serializer_class = CreateTeacherSerializer
    message = "Professor criado com sucesso. Por favor, verifique seu email."
