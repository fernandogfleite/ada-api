from rest_framework import (
    status,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ValidationError

from api.apps.authentication.models.user import (
    Secretary,
    Student,
    Teacher,
    User,
    UserConfirmation
)
from api.apps.authentication.permissions import IsSecretary
from api.apps.authentication.serializers.user import (
    CreateSecretarySerializer,
    CreateStudentSerializer,
    CreateTeacherSerializer,
    SecretarySerializer,
    StudentSerializer,
    TeacherSerializer
)
from api.apps.authentication.signals import send_email_confirmation


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


class StudentRegisterViewSet(CreateUserViewSet):
    serializer_class = CreateStudentSerializer
    message = "Estudante criado com sucesso. Por favor, verifique seu email."


class SecretaryRegisterViewSet(CreateUserViewSet):
    serializer_class = CreateSecretarySerializer
    message = "Secretário criado com sucesso. Por favor, verifique seu email."


class TeacherRegisterViewSet(CreateUserViewSet):
    permission_classes = [IsAuthenticated, IsSecretary]
    serializer_class = CreateTeacherSerializer
    message = "Professor criado com sucesso. Por favor, verifique seu email."


class UserConfirmView(APIView):
    serializer_class = None

    def post(self, request, token, format=None):
        try:
            user_confirm = UserConfirmation.objects.get(
                token=token
            )

            user = user_confirm.user

            if user.is_confirmed:
                return Response(
                    {
                        "message": "Usuário já confirmado."
                    },
                    status=status.HTTP_200_OK,
                )

            user.is_confirmed = True
            user.save()

        except UserConfirmation.DoesNotExist:
            raise ValidationError(
                detail={
                    "detail": "Código de confirmação inválido."
                }
            )

        return Response(
            {
                "message": "Usuário confirmado com sucesso. Agora você pode fazer login."
            },
            status=status.HTTP_200_OK
        )


class UserResendConfirmView(APIView):
    serializer_class = None

    def post(self, request, format=None):
        email = request.data.get("email", None)

        if not email:
            raise ValidationError(
                detail={
                    "detail": "Email é obrigatório."
                },
            )

        try:
            user = User.objects.get(email=email)

            if user.is_confirmed:
                return Response(
                    {
                        "message": "Usuário já confirmado."
                    },
                    status=status.HTTP_200_OK,
                )

            user_confirm = UserConfirmation.objects.get(user=user)
            send_email_confirmation(
                sender=UserConfirmation,
                instance=user_confirm,
                created=True,
            )

        except User.DoesNotExist:
            pass

        return Response(
            {
                "message": "Confirmação de email reenviada com sucesso. Por favor, verifique seu email."
            },
            status=status.HTTP_200_OK
        )


class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None
    model = None

    def get(self, request, format=None):
        if request.user.is_student:
            self.serializer_class = StudentSerializer
            self.model = Student

        elif request.user.is_teacher:
            self.serializer_class = TeacherSerializer
            self.model = Teacher

        elif request.user.is_secretary:
            self.serializer_class = SecretarySerializer
            self.model = Secretary

        instance = self.model.objects.get(user=request.user)
        serializer = self.serializer_class(instance)

        return Response(serializer.data)
