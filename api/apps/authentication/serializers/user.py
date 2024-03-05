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
    student_id = serializers.CharField(write_only=True)

    def validate_student_id(self, value):
        if Student.objects.filter(student_id=value).exists():
            raise serializers.ValidationError("Student ID already exists.")

        return value

    def create(self, validated_data):
        instance = Student.objects.create_student(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            student_id=validated_data['student_id']
        )

        return {
            "email": instance.user.email,
            "name": instance.user.name,
            "student_id": instance.student_id,
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
    teacher_id = serializers.CharField(write_only=True)

    def create(self, validated_data):
        instance = Teacher.objects.create_teacher(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            teacher_id=validated_data['teacher_id']
        )

        return {
            "email": instance.user.email,
            "name": instance.user.name,
            "teacher_id": instance.teacher_id,
        }

    def validate_teacher_id(self, value):
        if Teacher.objects.filter(teacher_id=value).exists():
            raise serializers.ValidationError("Teacher ID already exists.")

        return value


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
    secretary_id = serializers.CharField(write_only=True)

    def create(self, validated_data):
        instance = Secretary.objects.create_secretary(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            secretary_id=validated_data['secretary_id']
        )

        return {
            "email": instance.user.email,
            "name": instance.user.name,
            "secretary_id": instance.secretary_id,
        }

    def validate_secretary_id(self, value):
        if Secretary.objects.filter(secretary_id=value).exists():
            raise serializers.ValidationError("Secretary ID already exists.")

        return value


class StudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Student
        fields = (
            'name',
            'email',
            'student_id',
        )


class TeacherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Teacher
        fields = (
            'name',
            'email',
            'teacher_id',
        )


class SecretarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='user.name')
    email = serializers.EmailField(source='user.email')

    class Meta:
        model = Secretary
        fields = (
            'name',
            'email',
            'secretary_id'
        )
