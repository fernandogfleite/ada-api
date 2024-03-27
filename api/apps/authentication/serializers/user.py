from api.apps.authentication.models.user import (
    Student,
    Teacher,
    Secretary,
    User
)

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator


class JWTSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        if not self.user.is_confirmed:
            raise serializers.ValidationError(
                {
                    "message": "User is not confirmed yet. Please check your email."
                }
            )

        data['is_student'] = self.user.is_student
        data['is_teacher'] = self.user.is_teacher
        data['is_secretary'] = self.user.is_secretary

        return data


class CreateStudentSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Invalid email - user already exists."
            )
        ]
    )
    password = serializers.CharField(write_only=True)
    registration_id = serializers.CharField(write_only=True)

    def validate_registration_id(self, value):
        if Student.objects.filter(registration_id=value).exists():
            raise serializers.ValidationError(
                {
                    "registration_id": "Número de matrícula já cadastrado."
                }
            )

        return value

    def create(self, validated_data):
        instance = Student.objects.create_student(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            registration_id=validated_data['registration_id']
        )

        return {
            "email": instance.user.email,
            "name": instance.user.name,
            "registration_id": instance.registration_id,
        }


class CreateTeacherSerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Invalid email - user already exists."
            )
        ]
    )
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        instance = Teacher.objects.create_teacher(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return {
            "email": instance.user.email,
            "name": instance.user.name
        }


class CreateSecretarySerializer(serializers.Serializer):
    name = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message="Invalid email - user already exists."
            )
        ]
    )
    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        instance = Secretary.objects.create_secretary(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return {
            "email": instance.user.email,
            "name": instance.user.name
        }


class StudentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    role = serializers.CharField(source='user.role')

    class Meta:
        model = Student
        fields = (
            'id',
            'name',
            'email',
            'registration_id',
            'role'
        )


class TeacherSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    role = serializers.CharField(source='user.role')

    class Meta:
        model = Teacher
        fields = (
            'id',
            'name',
            'email',
            'role'
        )


class SecretarySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(source='user.id')
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')
    role = serializers.CharField(source='user.role')

    class Meta:
        model = Secretary
        fields = (
            'id',
            'name',
            'email',
            'role'
        )


class UpdateUserSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    registration_id = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = (
            "name",
            "email",
            "registration_id"
        )

    def validate_email(self, value):
        if self.instance.email != value and User.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                {
                    "email": "Email já cadastrado."
                }
            )

        return value

    def validate_registration_id(self, value):
        if self.instance.is_student and Student.objects.filter(
            registration_id=value
        ).exclude(user=self.instance).exists():
            raise serializers.ValidationError(
                {
                    "registration_id": "Número de matrícula já cadastrado."
                }
            )

        return value

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.email = validated_data.get('email', instance.email)

        instance.save()

        if instance.is_student:
            student = instance.student
            student.registration_id = validated_data.get(
                'registration_id',
                student.registration_id
            )
            student.save()

        return instance

    def to_representation(self, instance):
        if instance.is_student:
            return StudentSerializer(instance.student).data

        if instance.is_teacher:
            return TeacherSerializer(instance.teacher).data

        if instance.is_secretary:
            return SecretarySerializer(instance.secretary).data

        return super().to_representation(instance)


class UserChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "password",
            "new_password",
        )

    def update(self, instance, validated_data) -> User:
        if not instance.check_password(validated_data['password']):
            raise serializers.ValidationError(
                {
                    "password": "Senha incorreta."
                }
            )

        instance.set_password(validated_data['new_password'])
        instance.save()

        return instance
