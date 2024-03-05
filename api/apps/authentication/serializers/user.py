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


class CreateStudentSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    email = email = serializers.EmailField(
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

    def create(self, validated_data):
        return Student.objects.create_student(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            student_id=validated_data['student_id']
        )


class CreateTeacherSerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    email = email = serializers.EmailField(
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
        return Teacher.objects.create_teacher(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            teacher_id=validated_data['teacher_id']
        )


class CreateSecretarySerializer(serializers.ModelSerializer):
    name = serializers.CharField(write_only=True)
    email = email = serializers.EmailField(
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
        return Secretary.objects.create_secretary(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password'],
            secretary_id=validated_data['secretary_id']
        )
